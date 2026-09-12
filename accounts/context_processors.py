from django.core.cache import cache
from django.utils.translation import get_language

from accounts.models import SiteSettings
from news.category_labels import build_category_label_map
from news.services import list_categories

CACHE_SITE_SETTINGS = 'site_settings_solo'
CACHE_TTL = 60 * 5


def site_context(request):
    settings = cache.get(CACHE_SITE_SETTINGS)
    if settings is None:
        settings = SiteSettings.objects.first()
        cache.set(CACHE_SITE_SETTINGS, settings, CACHE_TTL)

    categories = list_categories()
    lang = get_language()
    return {
        'settings': settings,
        'all_categories': categories,
        'main_categories': categories[:3],
        'more_categories': categories[3:],
        'category_labels': build_category_label_map(categories, lang),
    }
