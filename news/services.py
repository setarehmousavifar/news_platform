from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.db.models import F, Count, Q, Case, When, IntegerField
from django.db.models.expressions import RawSQL

from .models import News, Category

CACHE_CATEGORIES = 'categories_all'
CACHE_LATEST = 'news_latest_{limit}'
CACHE_FEATURED = 'news_featured_{limit}'
CACHE_TRENDING = 'news_trending_{limit}'
CACHE_AUTH_STORY_COUNT = 'auth_stat_stories'
CACHE_TTL = getattr(settings, 'CACHE_TTL_SECONDS', 300)


def _cache_key(template, **kwargs):
    return template.format(**kwargs)


def get_published_news():
    """Lightweight queryset for lists — no reaction annotations."""
    return (
        News.objects.filter(status=News.Status.PUBLISHED)
        .select_related('author')
        .prefetch_related('categories')
        .defer('video')
    )


def get_published_news_with_reactions():
    """Detail/search views that need like/dislike counts."""
    return get_published_news().annotate(
        like_count=Count('liked_by', filter=Q(liked_by__is_like=True), distinct=True),
        dislike_count=Count('liked_by', filter=Q(liked_by__is_like=False), distinct=True),
    )


def get_trending_news(limit=5):
    key = _cache_key(CACHE_TRENDING, limit=limit)
    cached_ids = cache.get(key)
    if cached_ids is not None:
        news_map = {n.id: n for n in get_published_news().filter(id__in=cached_ids)}
        return [news_map[i] for i in cached_ids if i in news_map]

    qs = list(
        get_published_news().order_by('-views_count', '-published_date')[:limit]
    )
    cache.set(key, [n.id for n in qs], CACHE_TTL)
    return qs


def get_featured_news(limit=5):
    key = _cache_key(CACHE_FEATURED, limit=limit)
    cached_ids = cache.get(key)
    if cached_ids is not None:
        news_map = {n.id: n for n in get_published_news().filter(id__in=cached_ids)}
        return [news_map[i] for i in cached_ids if i in news_map]

    qs = list(
        get_published_news()
        .exclude(image='')
        .exclude(image__isnull=True)
        .order_by('-published_date')[:limit]
    )
    cache.set(key, [n.id for n in qs], CACHE_TTL)
    return qs


def get_latest_news(limit=10):
    key = _cache_key(CACHE_LATEST, limit=limit)
    cached_ids = cache.get(key)
    if cached_ids is not None:
        news_map = {n.id: n for n in get_published_news().filter(id__in=cached_ids)}
        return [news_map[i] for i in cached_ids if i in news_map]

    qs = list(get_published_news().order_by('-published_date')[:limit])
    cache.set(key, [n.id for n in qs], CACHE_TTL)
    return qs


def get_fresh_latest_news(limit=10):
    """Latest published stories without ID cache (admin or freshness-critical)."""
    return list(get_published_news().order_by('-published_date')[:limit])


def get_related_news(news, limit=5):
    tag_ids = list(news.tags.values_list('id', flat=True))
    category_ids = list(news.categories.values_list('id', flat=True))
    if not tag_ids and not category_ids:
        return News.objects.none()

    qs = get_published_news().exclude(id=news.id)
    if tag_ids:
        qs = (
            qs.filter(Q(tags__in=tag_ids) | Q(categories__in=category_ids))
            .annotate(shared_tags=Count('tags', filter=Q(tags__in=tag_ids), distinct=True))
            .order_by('-shared_tags', '-published_date')
            .distinct()
        )
    else:
        qs = qs.filter(categories__in=category_ids).distinct().order_by('-published_date')
    return qs[:limit]


def get_published_story_count():
    count = cache.get(CACHE_AUTH_STORY_COUNT)
    if count is None:
        count = News.objects.filter(status=News.Status.PUBLISHED).count()
        cache.set(CACHE_AUTH_STORY_COUNT, count, CACHE_TTL)
    return count


def increment_views(news_id):
    buffer_key = f'news_views_buffer_{news_id}'
    count = cache.get(buffer_key, 0) + 1
    flush_every = getattr(settings, 'VIEW_COUNT_FLUSH_EVERY', 5)
    if count >= flush_every:
        News.objects.filter(pk=news_id).update(views_count=F('views_count') + count)
        cache.delete(buffer_key)
    else:
        cache.set(buffer_key, count, timeout=60 * 60)


def create_news_item(*, author, form):
    news = form.save(commit=False)
    news.author = author
    if not news.status:
        news.status = News.Status.PUBLISHED
    news.save()
    form.save_m2m()
    manual_keywords = form.cleaned_data.get('keywords') or []
    if manual_keywords:
        form.apply_keywords(news)
    if news.status == News.Status.PUBLISHED:
        from .tagging import sync_news_tags
        sync_news_tags(news, merge_existing=True, extra_names=manual_keywords)
    invalidate_news_caches()
    index_news_document(news)
    return news


def soft_delete_news(news):
    news.soft_delete()
    invalidate_news_caches()
    remove_news_document(news.id)
    return news


def list_categories():
    categories = cache.get(CACHE_CATEGORIES)
    if categories is None:
        categories = list(Category.objects.all())
        cache.set(CACHE_CATEGORIES, categories, CACHE_TTL)
    return categories


def invalidate_news_caches():
    from django.core.cache.utils import make_template_fragment_key

    cache.delete(CACHE_CATEGORIES)
    cache.delete(CACHE_AUTH_STORY_COUNT)
    for lang in ('en', 'fa'):
        cache.delete(make_template_fragment_key('home_magazine', [lang]))
    for limit in (5, 6, 8, 10, 12, 16, 20):
        cache.delete(_cache_key(CACHE_LATEST, limit=limit))
        cache.delete(_cache_key(CACHE_FEATURED, limit=limit))
        cache.delete(_cache_key(CACHE_TRENDING, limit=limit))


def _supports_fulltext():
    return connection.vendor in ('mysql',)


def get_meili_client():
    url = getattr(settings, 'MEILI_URL', '') or ''
    if not url:
        return None
    try:
        import meilisearch
        return meilisearch.Client(url, getattr(settings, 'MEILI_MASTER_KEY', '') or None)
    except Exception:
        return None


def index_news_document(news):
    client = get_meili_client()
    if client is None:
        return False
    try:
        index = client.index(settings.MEILI_NEWS_INDEX)
        index.add_documents([{
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'slug': news.slug or '',
            'status': news.status,
        }])
        return True
    except Exception:
        return False


def remove_news_document(news_id):
    client = get_meili_client()
    if client is None:
        return False
    try:
        client.index(settings.MEILI_NEWS_INDEX).delete_document(news_id)
        return True
    except Exception:
        return False


def _meilisearch_ids(query, limit=50):
    client = get_meili_client()
    if client is None:
        return None
    try:
        result = client.index(settings.MEILI_NEWS_INDEX).search(query, {'limit': limit})
        return [hit['id'] for hit in result.get('hits', [])]
    except Exception:
        return None


def _fulltext_search(qs, query):
    boolean_query = ' '.join(f'+{term}*' for term in query.split() if term)
    if not boolean_query:
        return qs.none()
    return (
        qs.annotate(
            relevance=RawSQL(
                'MATCH(title, content) AGAINST(%s IN BOOLEAN MODE)',
                (boolean_query,),
            )
        )
        .filter(relevance__gt=0)
        .order_by('-relevance', '-published_date')
    )


def _order_by_ids(qs, ids):
    if not ids:
        return qs.none()
    whens = [When(id=pk, then=pos) for pos, pk in enumerate(ids)]
    return (
        qs.filter(id__in=ids)
        .annotate(search_rank=Case(*whens, default=9999, output_field=IntegerField()))
        .order_by('search_rank')
    )


def search_news(query=None, category_id=None, sort='latest'):
    """
    Search strategy (in order):
    1. Meilisearch (if MEILI_URL configured and reachable)
    2. MySQL FULLTEXT MATCH AGAINST
    3. Fallback icontains
    Always returns a QuerySet (pagination-safe).
    """
    qs = get_published_news()
    used_fulltext = False
    meili_ids = None

    if query:
        meili_ids = _meilisearch_ids(query)
        if meili_ids is not None:
            qs = _order_by_ids(qs, meili_ids)
        elif _supports_fulltext():
            try:
                ft_qs = _fulltext_search(qs, query)
                if ft_qs[:1]:
                    qs = ft_qs
                    used_fulltext = True
                else:
                    qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))
            except Exception:
                qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))
        else:
            qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))

    if category_id:
        try:
            category_pk = int(category_id)
        except (TypeError, ValueError):
            category_pk = None
        if category_pk is not None:
            qs = qs.filter(categories__id=category_pk)

    if sort == 'popular':
        return qs.order_by('-views_count', '-published_date')
    if used_fulltext:
        return qs
    if query and meili_ids is not None:
        return qs
    return qs.order_by('-published_date')
