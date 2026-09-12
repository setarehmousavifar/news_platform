from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Exists, OuterRef, Subquery
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import ListView
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from drf_spectacular.utils import extend_schema

from accounts.permissions import admin_required, can_edit_news, can_delete_news
from interactions.forms import CommentForm
from interactions.services import get_news_comments
from .forms import NewsForm, NewsInlineImageFormSet
from .models import News, Category
from .serializers import NewsSerializer
from . import services


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 6

    def get_queryset(self):
        return services.search_news(
            query=self.request.GET.get('q'),
            category_id=self.request.GET.get('category'),
            sort=self.request.GET.get('sort', 'latest'),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = services.list_categories()
        context['query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'latest') or 'latest'
        context['current_category'] = self.request.GET.get('category', '')
        return context


news_list = NewsListView.as_view()


@login_required
@admin_required
def manage_news(request):
    qs = News.objects.select_related('author').order_by('-updated_at')
    if request.user.user_type != 'super_admin':
        qs = qs.filter(author=request.user)

    query = (request.GET.get('q') or '').strip()
    current_status = (request.GET.get('status') or '').strip()
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if current_status in dict(News.Status.choices):
        qs = qs.filter(status=current_status)

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'accounts/manage_news.html', {
        'news_items': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'current_status': current_status,
        'status_choices': News.Status.choices,
    })


@login_required
@admin_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        formset = NewsInlineImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            news = services.create_news_item(author=request.user, form=form)
            formset.instance = news
            formset.save()
            messages.success(request, 'News created successfully.')
            if news.status == News.Status.PUBLISHED:
                return redirect('news_detail', slug=news.slug)
            return redirect('edit_news', pk=news.pk)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
        return render(
            request,
            'news/create_news.html',
            {
                'form': form,
                'inline_formset': formset,
                'categories': services.list_categories(),
            },
        )

    form = NewsForm()
    formset = NewsInlineImageFormSet()
    return render(
        request,
        'news/create_news.html',
        {
            'form': form,
            'inline_formset': formset,
            'categories': services.list_categories(),
        },
    )


@login_required
@admin_required
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if not can_edit_news(request.user, news):
        raise PermissionDenied('You do not have permission to edit this news item.')

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        formset = NewsInlineImageFormSet(request.POST, request.FILES, instance=news)
        if form.is_valid() and formset.is_valid():
            news = form.save()
            formset.save()
            manual_keywords = form.cleaned_data.get('keywords') or []
            if manual_keywords:
                form.apply_keywords(news)
            if news.status == News.Status.PUBLISHED:
                from .tagging import sync_news_tags
                sync_news_tags(news, merge_existing=True, extra_names=manual_keywords)
            messages.success(request, 'News updated successfully.')
            return redirect('manage_news')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
    else:
        form = NewsForm(instance=news)
        formset = NewsInlineImageFormSet(instance=news)
    return render(
        request,
        'news/edit_news.html',
        {
            'form': form,
            'inline_formset': formset,
            'news': news,
            'categories': services.list_categories(),
        },
    )


@login_required
@admin_required
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if not can_delete_news(request.user, news):
        raise PermissionDenied('You do not have permission to delete this news item.')

    if request.method == 'POST':
        services.soft_delete_news(news)
        messages.success(request, 'News archived (soft-deleted).')
        return redirect('manage_news')
    return render(request, 'news/delete_news.html', {'news': news})


def news_detail(request, slug):
    from interactions.models import SavedArticle, Like, Comment

    qs = services.get_published_news_with_reactions().prefetch_related('categories', 'tags')
    if request.user.is_authenticated:
        qs = qs.annotate(
            user_has_saved=Exists(
                SavedArticle.objects.filter(user=request.user, news_id=OuterRef('pk'))
            ),
            user_reaction_is_like=Subquery(
                Like.objects.filter(user=request.user, news_id=OuterRef('pk')).values('is_like')[:1]
            ),
        )

    news = get_object_or_404(qs, slug=slug)
    services.increment_views(news.pk)

    total_likes = getattr(news, 'like_count', news.total_likes())
    total_dislikes = getattr(news, 'dislike_count', news.total_dislikes())
    related_news = services.get_related_news(news)
    comments = get_news_comments(news, user=request.user)

    user_reaction = None
    is_saved = False
    if request.user.is_authenticated:
        is_like = getattr(news, 'user_reaction_is_like', None)
        if is_like is True:
            user_reaction = 'like'
        elif is_like is False:
            user_reaction = 'dislike'
        is_saved = bool(getattr(news, 'user_has_saved', False))

    user_has_liked = user_reaction == 'like'
    trending_sidebar = services.get_trending_news(limit=6)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            login_url = reverse('login')
            return redirect(f'{login_url}?next={request.path}')
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent = None
            if parent_id:
                parent = Comment.objects.filter(id=parent_id, news=news, parent=None).first()
                if not parent:
                    messages.error(request, 'Invalid reply target.')
                    return redirect('news_detail', slug=news.slug)

            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = news
            comment.parent = parent
            comment.save()
            messages.success(request, 'Comment posted.')
            return redirect('news_detail', slug=news.slug)
        messages.error(request, 'Please correct your comment and try again.')
    else:
        form = CommentForm()

    return render(request, 'news/news_detail.html', {
        'news': news,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'user_has_liked': user_has_liked,
        'user_reaction': user_reaction,
        'is_saved': is_saved,
        'related_news': related_news,
        'trending_sidebar': trending_sidebar,
        'comments': comments,
        'form': form,
    })


class NewsAPIThrottle(AnonRateThrottle):
    rate = '60/minute'


@extend_schema(exclude=True)
@api_view(['GET'])
@throttle_classes([NewsAPIThrottle, UserRateThrottle])
def news_list_api(request):
    """Deprecated: use /api/v1/news/ (paginated). Kept for backward compatibility."""
    news = services.get_published_news().order_by('-published_date')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(news, request)
    serializer = NewsSerializer(page, many=True)
    response = paginator.get_paginated_response(serializer.data)
    response['Deprecation'] = 'true'
    response['Link'] = '</api/v1/news/>; rel="successor-version"'
    return response


@extend_schema(exclude=True)
@api_view(['GET'])
@throttle_classes([NewsAPIThrottle, UserRateThrottle])
def news_detail_api(request, pk):
    """Deprecated: use /api/v1/news/<slug>/."""
    news = get_object_or_404(services.get_published_news(), pk=pk)
    serializer = NewsSerializer(news)
    response = Response(serializer.data)
    response['Deprecation'] = 'true'
    response['Link'] = f'</api/v1/news/{news.slug}/>; rel="successor-version"'
    return response



def category_news(request, category_slug):
    category = Category.objects.filter(slug=category_slug).first()
    if category is None:
        category = get_object_or_404(Category, name__iexact=category_slug)
    qs = (
        services.get_published_news()
        .filter(categories=category)
        .order_by('-published_date')
    )
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'news/category_news.html', {
        'news_list': page_obj.object_list,
        'page_obj': page_obj,
        'category_name': category.name,
        'category': category,
    })


def tag_news(request, tag_slug):
    from .models import Tag

    tag = Tag.objects.filter(slug=tag_slug).first()
    if tag is None:
        tag = get_object_or_404(Tag, name__iexact=tag_slug.replace('-', ' '))
    qs = (
        services.get_published_news()
        .filter(tags=tag)
        .order_by('-published_date')
    )
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'news/tag_news.html', {
        'news_list': page_obj.object_list,
        'page_obj': page_obj,
        'tag': tag,
    })


def health_check(request):
    """Lightweight readiness probe for ops/monitoring."""
    from django.db import connection
    from news.services import get_meili_client, _supports_fulltext

    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    search_backend = 'icontains'
    if get_meili_client() is not None:
        search_backend = 'meilisearch'
    elif _supports_fulltext():
        search_backend = 'mysql_fulltext'

    cache_backend = settings.CACHES['default']['BACKEND'].split('.')[-1]

    status_code = 200 if db_ok else 503
    return JsonResponse(
        {
            'status': 'ok' if db_ok else 'degraded',
            'database': db_ok,
            'cache': cache_backend,
            'search': search_backend,
            'service': 'news_platform',
        },
        status=status_code,
    )
