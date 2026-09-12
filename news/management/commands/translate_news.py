from django.core.management.base import BaseCommand

from django.core.cache import cache

from news.models import News, Category, Tag
from news.translation_service import (
    CACHE_TTL,
    clear_invalid_translations,
    ensure_news_translations,
    translate_text,
    _cache_key,
    is_persian_text,
    _is_valid_translation,
)


class Command(BaseCommand):
    help = 'Generate or refresh auto-translations for published news.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Re-translate even if cached')
        parser.add_argument('--limit', type=int, default=0, help='Max stories to process')
        parser.add_argument('--clear', action='store_true', help='Clear invalid translations first')

    def handle(self, *args, **options):
        qs = News.objects.filter(is_deleted=False, status=News.Status.PUBLISHED).order_by('-published_date')
        if options['limit']:
            qs = qs[: options['limit']]
        total = qs.count()
        self.stdout.write(f'Translating {total} stories…')
        for i, news in enumerate(qs, start=1):
            if options['clear'] or options['force']:
                clear_invalid_translations(news)
            ensure_news_translations(news, force=options['force'])
            fa = (news.translations or {}).get('fa', {})
            ok = bool(fa.get('title') and is_persian_text(fa.get('title', '')))
            self.stdout.write(f'  [{i}/{total}] {news.pk}: {"OK" if ok else "FAIL"}')

        self.stdout.write('Warming tag & category caches…')
        for tag in Tag.objects.all():
            name = tag.name
            if name and not is_persian_text(name):
                key = _cache_key(name, 'fa', 'en')
                if options['force'] or not cache.get(key):
                    cache.set(key, translate_text(name, 'fa', 'en'), CACHE_TTL)
        for cat in Category.objects.all():
            display = (cat.name or '').replace('_', ' ').title()
            if display and not is_persian_text(display):
                ckey = f'cat_tr:fa:{cat.pk}:{cat.name}'
                if options['force'] or not cache.get(ckey):
                    translated = translate_text(display, 'fa', 'en')
                    cache.set(ckey, translated, CACHE_TTL)
                    cache.set(_cache_key(display, 'fa', 'en'), translated, CACHE_TTL)

        self.stdout.write(self.style.SUCCESS('Done.'))
