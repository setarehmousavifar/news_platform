from django import template
from django.utils import timezone
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
import json
import re

register = template.Library()

PERSIAN_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
INLINE_IMAGE_RE = re.compile(r'\[inline:(\d+)\]', re.IGNORECASE)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Build a query string from the current GET params, overriding keys in kwargs.
    Pass None to remove a key. Example: ?{% url_replace sort='popular' page=None %}
    """
    request = context.get('request')
    if request is None:
        return ''
    query = request.GET.copy()
    for key, value in kwargs.items():
        if value is None or value == '':
            query.pop(key, None)
        else:
            query[key] = value
    return query.urlencode()


@register.simple_tag(takes_context=True)
def absolute_url(context, path=None):
    """Build an absolute URL for Open Graph / canonical tags."""
    request = context.get('request')
    if request is None:
        return path or '/'
    if path:
        return request.build_absolute_uri(path)
    return request.build_absolute_uri()


@register.filter
def truncate_meta(value, length=160):
    text = ' '.join((value or '').split())
    if len(text) <= length:
        return text
    return text[: length - 1].rstrip() + '…'


@register.filter
def topic_label(value):
    """Human-readable topic name, localized when needed (no DB/API)."""
    from news.category_labels import get_category_label
    from django.utils import translation as dj_trans

    lang = (dj_trans.get_language() or 'en').split('-')[0]
    if hasattr(value, 'name'):
        return get_category_label(value.name, lang)
    return get_category_label(str(value or '').strip(), lang)


@register.filter
def localized_excerpt(news, length=160):
    """Short localized summary without rendering full HTML body."""
    text = (news.localized_content() or '').replace('\n', ' ').strip()
    if len(text) <= length:
        return text
    return text[: length - 1].rstrip() + '…'


@register.filter
def localized_title(news):
    return news.localized_title()


@register.filter
def localized_content(news):
    return news.localized_content()


@register.filter
def content_dir(lang=None):
    """Return rtl/ltr for current or given language."""
    from django.utils import translation as dj_trans
    code = (lang or dj_trans.get_language() or 'en').split('-')[0]
    return 'rtl' if code == 'fa' else 'ltr'


@register.filter
def elided_page_range(page_obj, on_each_side=2):
    """Paginator elided page range for compact pagination UI."""
    if not page_obj or not hasattr(page_obj, 'paginator'):
        return []
    return page_obj.paginator.get_elided_page_range(
        number=page_obj.number,
        on_each_side=int(on_each_side),
        on_ends=1,
    )


@register.filter
def has_persian(value):
    return bool(PERSIAN_RE.search(str(value or '')))


@register.filter
def news_time_ago(value):
    """Relative time for timeline widgets, e.g. 3 MINS AGO."""
    if not value:
        return ''
    now = timezone.now()
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())
    delta = now - value
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return _('JUST NOW')
    minutes = seconds // 60
    if minutes < 60:
        if minutes == 1:
            return _('1 MIN AGO')
        return _('%(minutes)s MINS AGO') % {'minutes': minutes}
    hours = minutes // 60
    if hours < 24:
        if hours == 1:
            return _('1 HR AGO')
        return _('%(hours)s HRS AGO') % {'hours': hours}
    days = hours // 24
    if days < 7:
        if days == 1:
            return _('1 DAY AGO')
        return _('%(days)s DAYS AGO') % {'days': days}
    return news_datetime(value)


@register.filter
def news_datetime(value):
    if not value:
        return ''
    now = timezone.localtime(timezone.now())
    dt = timezone.localtime(value)
    if dt.date() == now.date():
        return dt.strftime('%I:%M %p').lstrip('0').replace('AM', 'AM').replace('PM', 'PM')
    if dt.year == now.year:
        return dt.strftime('%b %d · %I:%M %p').replace(' 0', ' ')
    return dt.strftime('%b %d, %Y')


@register.filter
def reading_time(value):
    """Estimated reading time, e.g. 4 min read."""
    words = len(re.findall(r'\S+', str(value or '')))
    minutes = max(1, round(words / 210))
    return _('%(minutes)s min read') % {'minutes': minutes}


@register.filter
def localized_reading_time(news):
    return reading_time(news.localized_content())


@register.filter
def author_name(user):
    if not user:
        return ''
    full = user.get_full_name().strip()
    return full or user.username


@register.inclusion_tag('partials/_author_avatar.html')
def author_avatar(user, size='sm'):
    return {'user': user, 'size': size}


def _render_news_content_html(news, content=None):
    content = (content if content is not None else (news.content or '')).strip()
    if not content:
        return ''

    inline_map = {img.order: img for img in news.inline_images.all()}

    def inline_html(order):
        img = inline_map.get(int(order))
        if not img:
            return ''
        caption = f'<figcaption>{escape(img.caption)}</figcaption>' if img.caption else ''
        return (
            f'<figure class="article-inline-image">'
            f'<img src="{escape(img.image.url)}" alt="{escape(img.caption or news.title)}" loading="lazy" decoding="async">'
            f'{caption}</figure>'
        )

    segments = INLINE_IMAGE_RE.split(content)
    html_parts = []
    lead_assigned = False
    idx = 0
    while idx < len(segments):
        text = segments[idx]
        if text and not text.isdigit():
            for para in [p.strip() for p in text.split('\n\n') if p.strip()]:
                cls = ''
                if not lead_assigned:
                    cls = 'article-prose__lead'
                    lead_assigned = True
                class_attr = f' class="{cls}"' if cls else ''
                html_parts.append(format_html(
                    '<p{}>{}</p>',
                    mark_safe(class_attr),
                    mark_safe(escape(para).replace('\n', '<br>')),
                ))
        if idx + 1 < len(segments) and segments[idx + 1].isdigit():
            html_parts.append(mark_safe(inline_html(segments[idx + 1])))
            idx += 2
            continue
        idx += 1

    return mark_safe(''.join(str(part) for part in html_parts))


@register.filter
def render_news_content(news):
    return _render_news_content_html(news)


@register.filter
def localized_content_html(news):
    return _render_news_content_html(news, content=news.localized_content())


@register.simple_tag
def news_article_jsonld(news, page_url, image_url=''):
    """JSON-LD NewsArticle for a published story."""
    data = {
        '@context': 'https://schema.org',
        '@type': 'NewsArticle',
        'headline': news.title,
        'datePublished': news.published_date.isoformat() if news.published_date else None,
        'dateModified': news.updated_at.isoformat() if news.updated_at else None,
        'author': {
            '@type': 'Person',
            'name': str(news.author),
        },
        'mainEntityOfPage': {
            '@type': 'WebPage',
            '@id': page_url,
        },
        'url': page_url,
        'description': truncate_meta(news.content, 160),
    }
    if image_url:
        data['image'] = [image_url]
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'
    )
