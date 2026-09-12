from django.db import transaction
from django.db.models import Count, Q

from .models import Like, CommentLike, Comment, SavedArticle


def get_news_comments(news, user=None):
    qs = (
        Comment.objects.filter(news=news, parent=None)
        .select_related('user')
        .prefetch_related('replies__user', 'likes')
        .annotate(
            like_total=Count('likes', filter=Q(likes__is_like=True), distinct=True),
            dislike_total=Count('likes', filter=Q(likes__is_like=False), distinct=True),
        )
    )
    comments = list(qs)
    if user and user.is_authenticated:
        comment_ids = [c.id for c in comments]
        user_likes = {
            cl.comment_id: cl.is_like
            for cl in CommentLike.objects.filter(user=user, comment_id__in=comment_ids)
        }
        for comment in comments:
            reaction = user_likes.get(comment.id)
            comment.user_liked = reaction is True
            comment.user_disliked = reaction is False
    else:
        for comment in comments:
            comment.user_liked = False
            comment.user_disliked = False
    return comments


def toggle_news_like(user, news):
    """Legacy toggle — returns (liked: bool, total_likes: int)."""
    with transaction.atomic():
        like, created = Like.objects.get_or_create(user=user, news=news, defaults={'is_like': True})
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        total = news.liked_by.filter(is_like=True).count()
    return liked, total


def toggle_news_reaction(user, news, *, is_like=True):
    with transaction.atomic():
        existing = Like.objects.filter(user=user, news=news).first()
        liked = False
        disliked = False
        if existing:
            if existing.is_like == is_like:
                existing.delete()
            else:
                existing.is_like = is_like
                existing.save(update_fields=['is_like'])
                liked = is_like
                disliked = not is_like
        else:
            Like.objects.create(user=user, news=news, is_like=is_like)
            liked = is_like
            disliked = not is_like

    return {
        'liked': liked,
        'disliked': disliked,
        'total_likes': news.liked_by.filter(is_like=True).count(),
        'total_dislikes': news.liked_by.filter(is_like=False).count(),
    }


def toggle_comment_like(user, comment, is_like=True):
    with transaction.atomic():
        existing = CommentLike.objects.filter(user=user, comment=comment).first()
        removed = False
        liked = False
        disliked = False
        if existing:
            if existing.is_like == is_like:
                existing.delete()
                removed = True
            else:
                existing.is_like = is_like
                existing.save(update_fields=['is_like'])
                liked = is_like
                disliked = not is_like
        else:
            CommentLike.objects.create(user=user, comment=comment, is_like=is_like)
            liked = is_like
            disliked = not is_like

    return {
        'liked': liked,
        'disliked': disliked,
        'removed': removed,
        'total_likes': comment.likes.filter(is_like=True).count(),
        'total_dislikes': comment.likes.filter(is_like=False).count(),
    }


def toggle_saved_article(user, news):
    saved, created = SavedArticle.objects.get_or_create(user=user, news=news)
    if not created:
        saved.delete()
        return {'saved': False}
    return {'saved': True}
