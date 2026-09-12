"""Static category display names — no runtime API calls."""

from django.utils.translation import get_language

CATEGORY_LABELS_FA = {
    'breaking_news': 'اخبار فوری',
    'world': 'جهان',
    'politics': 'سیاست',
    'business': 'اقتصاد و کسب‌وکار',
    'economy': 'اقتصاد',
    'technology': 'فناوری',
    'science': 'علم',
    'health': 'سلامت',
    'sports': 'ورزش',
    'entertainment': 'سرگرمی',
    'culture': 'فرهنگ',
    'lifestyle': 'سبک زندگی',
    'opinion': 'دیدگاه',
    'education': 'آموزش',
    'environment': 'محیط زیست',
    'crime': 'جرم و جنایت',
    'travel': 'سفر',
    'food': 'غذا',
    'real_estate': 'املاک',
    'weather': 'آب و هوا',
    'video': 'ویدیو',
}


def _english_label(name: str) -> str:
    return (name or '').replace('_', ' ').replace('-', ' ').strip().title()


def get_category_label(name: str, lang: str | None = None) -> str:
    lang = (lang or get_language() or 'en').split('-')[0]
    key = (name or '').strip()
    if lang == 'fa':
        return CATEGORY_LABELS_FA.get(key, _english_label(key))
    return _english_label(key)


def build_category_label_map(categories, lang: str | None = None) -> dict[int, str]:
    """Map category pk → localized label for templates."""
    lang = (lang or get_language() or 'en').split('-')[0]
    return {cat.pk: get_category_label(cat.name, lang) for cat in categories}
