from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit

from .forms import (
    CustomUserCreationForm,
    UserProfileForm,
    UserEditForm,
    EditUserRoleForm,
    PasswordResetRequestForm,
    USERNAME_PATTERN,
)
from .models import CustomUser
from .permissions import admin_required, super_admin_required, can_manage_user
from .utils import get_safe_redirect_url
from .services import change_user_role


def _auth_page_context():
    """Visual context for login/register split layout."""
    from news import services

    featured = services.get_featured_news(limit=5) or services.get_latest_news(limit=5)
    headlines = [item.title for item in featured]

    settings_obj = None
    try:
        from .models import SiteSettings
        settings_obj = SiteSettings.objects.first()
    except Exception:
        pass

    tagline = (settings_obj.description if settings_obj else '') or 'Independent reporting and clear analysis from around the world.'
    if len(tagline) > 140:
        tagline = tagline[:137].rstrip() + '…'

    return {
        'auth_headlines': headlines or [
            'World headlines in real time',
            'Politics, business, technology',
            'Your voice in the conversation',
        ],
        'auth_tagline': tagline,
        'auth_stat_topics': len(services.list_categories()),
        'auth_stat_stories': services.get_published_story_count(),
    }


@login_required
@super_admin_required
def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/manage_users.html', {'users': users})


@login_required
@super_admin_required
def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if not can_manage_user(request.user, user):
        messages.error(request, 'You cannot manage this user.')
        return redirect('manage_users')
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user, actor=request.user)
        if form.is_valid():
            old_role = user.user_type
            form.save()
            if form.cleaned_data.get('user_type') != old_role:
                from .services import change_user_role
                # form already saved; write audit if role changed
                from .models import RoleAuditLog
                RoleAuditLog.objects.create(
                    actor=request.user,
                    target=user,
                    old_role=old_role,
                    new_role=form.cleaned_data['user_type'],
                    note='Edited via manage users form',
                )
            messages.success(request, 'User updated successfully.')
            return redirect('manage_users')
    else:
        form = UserEditForm(instance=user, actor=request.user)
    return render(request, 'accounts/edit_user.html', {'form': form})


@login_required
@super_admin_required
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if not can_manage_user(request.user, user):
        messages.error(request, 'You cannot delete this user.')
        return redirect('manage_users')
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('manage_users')
    return render(request, 'accounts/delete_user.html', {'target_user': user})


@login_required
@super_admin_required
def edit_user_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not can_manage_user(request.user, user):
        messages.error(request, 'You cannot manage this user.')
        return redirect('manage_users')
    if request.method == 'POST':
        form = EditUserRoleForm(request.POST, instance=user, actor=request.user)
        if form.is_valid():
            change_user_role(
                actor=request.user,
                target=user,
                new_role=form.cleaned_data['user_type'],
                note='Role change via role form',
            )
            messages.success(request, 'User role updated successfully!')
            return redirect('manage_users')
    else:
        form = EditUserRoleForm(instance=user, actor=request.user)
    return render(request, 'accounts/edit_user_role.html', {'form': form, 'target_user': user})


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@ensure_csrf_cookie
def register(request):
    if getattr(request, 'limited', False):
        messages.error(request, 'Too many registration attempts. Please try again later.')
        return render(request, 'accounts/register.html', {**_auth_page_context(), 'form': CustomUserCreationForm()})

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome aboard.')
            return get_safe_redirect_url(request, request.GET.get('next'))
        messages.error(request, 'Please fix the highlighted fields below to complete registration.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {**_auth_page_context(), 'form': form})


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@ensure_csrf_cookie
def user_login(request):
    if getattr(request, 'limited', False):
        messages.error(request, 'Too many login attempts. Please try again later.')
        return render(request, 'accounts/login.html', {**_auth_page_context(), 'form': AuthenticationForm()})

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.POST.get('remember_me'):
                request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                request.session.set_expiry(0)
            messages.success(request, 'You have successfully logged in.')
            return get_safe_redirect_url(request, request.GET.get('next'))
        messages.error(request, 'Invalid username or password. Please check your details and try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {**_auth_page_context(), 'form': form})


@ratelimit(key='ip', rate='30/m', method='GET', block=True)
@require_GET
def check_username(request):
    username = (request.GET.get('username') or '').strip()
    if not USERNAME_PATTERN.match(username):
        return JsonResponse({
            'available': False,
            'message': 'Username can only contain letters and numbers.',
        })
    if len(username) < 3:
        return JsonResponse({
            'available': False,
            'message': 'Username must be at least 3 characters.',
        })
    if len(username) > 150:
        return JsonResponse({
            'available': False,
            'message': 'Username must be 150 characters or fewer.',
        })
    available = not CustomUser.objects.filter(username__iexact=username).exists()
    return JsonResponse({
        'available': available,
        'message': 'Username is available.' if available else 'This username is already taken.',
    })


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def password_reset_request(request):
    if getattr(request, 'limited', False):
        messages.error(request, 'Too many reset attempts. Please try again later.')
        return render(request, 'accounts/password_reset.html', {'form': PasswordResetRequestForm()})

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            form.send_reset_email(request)
            messages.success(
                request,
                'If an account matches that username and email, you will receive reset instructions shortly.',
            )
            return redirect('password_reset_done')
        messages.error(request, 'Please enter both your username and a valid email address.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset.html', {'form': form})


@require_POST
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'accounts/profile.html', {
        **_auth_page_context(),
        'form': form,
        'show_avatar': user.is_publisher,
    })


@login_required
def saved_stories(request):
    from django.core.paginator import Paginator
    from interactions.models import SavedArticle

    qs = (
        SavedArticle.objects.filter(user=request.user)
        .select_related('news', 'news__author')
        .prefetch_related('news__categories', 'news__tags')
        .order_by('-created_at')
    )
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'accounts/saved_stories.html', {
        'saved_items': page_obj.object_list,
        'page_obj': page_obj,
    })


@login_required
@admin_required
def admin_dashboard(request):
    from django.db.models import Sum

    from news.models import News

    news_qs = News.objects.all()
    if request.user.user_type != 'super_admin':
        news_qs = news_qs.filter(author=request.user)

    stats = {
        'published': news_qs.filter(status=News.Status.PUBLISHED).count(),
        'drafts': news_qs.filter(status=News.Status.DRAFT).count(),
        'total_views': news_qs.aggregate(total=Sum('views_count'))['total'] or 0,
        'mine': news_qs.count(),
        'users': CustomUser.objects.count() if request.user.user_type == 'super_admin' else 0,
    }
    recent_news = list(news_qs.order_by('-updated_at')[:8])

    return render(request, 'accounts/admin_dashboard.html', {
        'stats': stats,
        'recent_news': recent_news,
    })


def home_view(request):
    from news import services
    from news.models import Category

    featured = services.get_featured_news(limit=8)
    latest = services.get_latest_news(limit=20)
    trending_news = services.get_trending_news(limit=5)
    popular_news = trending_news
    carousel_slides = featured[:5] if featured else latest[:5]
    hero = carousel_slides[0] if carousel_slides else None
    featured_ids = {item.id for item in carousel_slides}

    latest_timeline = latest[:6]

    world_cat = Category.objects.filter(slug='world').first()
    if world_cat:
        world_news = list(
            services.get_published_news()
            .filter(categories=world_cat)
            .exclude(id__in=featured_ids)[:4]
        )
    else:
        world_news = [n for n in latest if n.id not in featured_ids][:4]

    top_stories = [n for n in latest if n.id not in featured_ids][4:10]

    return render(request, 'home.html', {
        'hero': hero,
        'carousel_slides': carousel_slides,
        'trending_news': trending_news,
        'popular_news': popular_news,
        'world_news': world_news,
        'latest_timeline': latest_timeline,
        'top_stories': top_stories,
        'featured_news': featured,
    })
