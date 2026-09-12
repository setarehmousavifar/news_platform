from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from django_ratelimit.decorators import ratelimit

from .models import Comment
from .services import toggle_news_reaction, toggle_comment_like, toggle_saved_article
from news.models import News


@require_http_methods(['GET', 'POST'])
def add_comment(request, pk):
    """Legacy route: comments live on the article detail page."""
    news = get_object_or_404(News.objects.filter(status=News.Status.PUBLISHED), pk=pk)
    return redirect('news_detail', slug=news.slug)


@ratelimit(key='ip', rate='60/m', method='POST', block=True)
@require_POST
def like_news(request, news_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                'detail': 'Authentication required.',
                'login_url': reverse('login'),
            },
            status=401,
        )
    news = get_object_or_404(News.objects.filter(status=News.Status.PUBLISHED), id=news_id)
    is_like = request.POST.get('is_like', '1') != '0'
    result = toggle_news_reaction(request.user, news, is_like=is_like)
    return JsonResponse(result)


@login_required
@require_POST
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment.objects.select_related('news'), id=comment_id)
    if comment.user != request.user and request.user.user_type != 'super_admin':
        messages.error(request, 'You can only edit your own comments.')
        return redirect('news_detail', slug=comment.news.slug)
    content = request.POST.get('content', '').strip()
    if len(content) < 2:
        messages.error(request, 'Comment must be at least 2 characters.')
        return redirect('news_detail', slug=comment.news.slug)
    comment.content = content
    comment.save(update_fields=['content'])
    messages.success(request, 'Comment updated.')
    return redirect('news_detail', slug=comment.news.slug)


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment.objects.select_related('news'), id=comment_id)
    if comment.user != request.user and request.user.user_type != 'super_admin':
        messages.error(request, 'You can only delete your own comments.')
        return redirect('news_detail', slug=comment.news.slug)
    slug = comment.news.slug
    comment.delete()
    messages.success(request, 'Comment removed.')
    return redirect('news_detail', slug=slug)


@ratelimit(key='ip', rate='60/m', method='POST', block=True)
@require_POST
def like_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                'detail': 'Authentication required.',
                'login_url': reverse('login'),
            },
            status=401,
        )
    comment = get_object_or_404(
        Comment.objects.select_related('news').filter(news__status=News.Status.PUBLISHED),
        id=comment_id,
    )
    is_like = request.POST.get('is_like', '1') != '0'
    result = toggle_comment_like(request.user, comment, is_like=is_like)
    return JsonResponse(result)


@ratelimit(key='ip', rate='60/m', method='POST', block=True)
@require_POST
def toggle_save_article(request, news_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                'detail': 'Authentication required.',
                'login_url': reverse('login'),
            },
            status=401,
        )
    news = get_object_or_404(News.objects.filter(status=News.Status.PUBLISHED), id=news_id)
    result = toggle_saved_article(request.user, news)
    return JsonResponse(result)
