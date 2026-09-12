"""Auto-generate keyword tags from news title, content, and categories."""

from __future__ import annotations

import re

from django.utils.text import slugify

from .models import Tag

STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
    'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has',
    'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
    'must', 'shall', 'can', 'this', 'that', 'these', 'those', 'it', 'its', 'they',
    'them', 'their', 'we', 'our', 'you', 'your', 'he', 'she', 'his', 'her', 'not',
    'no', 'yes', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
    'such', 'than', 'too', 'very', 'just', 'about', 'into', 'through', 'during', 'before',
    'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'what',
    'which', 'who', 'whom', 'new', 'says', 'said', 'also', 'get', 'got', 'one', 'two',
    'first', 'last', 'year', 'years', 'day', 'days', 'time', 'news', 'story', 'stories',
    'read', 'like', 'make', 'made', 'many', 'much',
}

WORD_RE = re.compile(r'[\w\u0600-\u06FF]{3,}', re.UNICODE)
PERSIAN_RE = re.compile(r'[\u0600-\u06FF]')


def _normalize_keyword(word: str) -> str:
    word = word.strip().lower()
    if not word or word in STOP_WORDS or word.isdigit():
        return ''
    if PERSIAN_RE.search(word):
        return word
    if len(word) < 3:
        return ''
    return word.title()


def _extract_words(text: str, limit: int = 6) -> list[str]:
    seen: set[str] = set()
    keywords: list[str] = []
    for match in WORD_RE.findall((text or '').lower()):
        normalized = _normalize_keyword(match)
        if not normalized or normalized.lower() in seen:
            continue
        seen.add(normalized.lower())
        keywords.append(normalized)
        if len(keywords) >= limit:
            break
    return keywords


def collect_keywords(news) -> list[str]:
    keywords: list[str] = []
    seen: set[str] = set()

    def add(value: str):
        normalized = _normalize_keyword(value)
        if not normalized:
            return
        key = normalized.lower()
        if key in seen:
            return
        seen.add(key)
        keywords.append(normalized)

    for category in news.categories.all():
        add(category.name.replace('_', ' ').replace('-', ' '))

    for word in _extract_words(news.title, limit=5):
        add(word)

    for word in _extract_words((news.content or '')[:800], limit=4):
        add(word)

    return keywords[:8]


def get_or_create_tag(name: str) -> Tag:
    slug_base = slugify(name) or 'tag'
    tag = Tag.objects.filter(slug=slug_base).first()
    if tag:
        return tag
    tag = Tag.objects.filter(name__iexact=name).first()
    if tag:
        return tag
    return Tag.objects.create(name=name)


def sync_news_tags(news, *, merge_existing: bool = True, extra_names: list[str] | None = None) -> list[Tag]:
    """Assign keyword tags to a news item (auto + optional manual names)."""
    if news.status != news.Status.PUBLISHED or news.is_deleted:
        return list(news.tags.all())

    names: list[str] = []
    seen: set[str] = set()

    def add_name(value: str):
        normalized = (value or '').strip()
        if not normalized:
            return
        key = normalized.casefold()
        if key in seen:
            return
        seen.add(key)
        names.append(normalized[:80])

    if extra_names:
        for name in extra_names:
            add_name(name)

    if merge_existing:
        for name in news.tags.values_list('name', flat=True):
            add_name(name)

    for name in collect_keywords(news):
        add_name(name)

    tags = [get_or_create_tag(name) for name in names[:12]]
    news.tags.set(tags)
    return tags
