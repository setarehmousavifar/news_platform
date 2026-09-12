"""
Populate the database with premium bilingual-ready English news content.
Usage: python manage.py seed_premium --purge
"""

from __future__ import annotations

import io
import urllib.request
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models.signals import post_save
from django.utils import timezone

from accounts.models import CustomUser, SiteSettings
from news.models import Category, News, Tag
from news.seed_data.premium_catalog import AUTHORS, CATEGORY_NAMES, get_all_articles
from news.seed_data.premium_images import image_url
from news.services import invalidate_news_caches, index_news_document
from news.signals import news_saved
from news.tagging import sync_news_tags

USER_AGENT = 'nevox-news-seeder/1.0'


class Command(BaseCommand):
    help = 'Seed premium English news articles with images, tags, and homepage-ready metrics.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--purge',
            action='store_true',
            help='Remove existing news articles before seeding.',
        )
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help='Skip downloading Unsplash images (faster, but carousel needs images).',
        )
        parser.add_argument(
            '--skip-translate',
            action='store_true',
            help='Skip automatic Persian translation after seeding.',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('nevox premium seed — starting'))

        self._ensure_site_settings()
        categories = self._ensure_categories()
        authors = self._ensure_authors()

        if options['purge']:
            deleted = News.all_objects.count()
            News.all_objects.all().delete()
            Tag.objects.all().delete()
            invalidate_news_caches()
            cache.clear()
            self.stdout.write(self.style.WARNING(f'Purged {deleted} existing news items.'))

        articles = get_all_articles()
        created = 0

        post_save.disconnect(news_saved, sender=News)
        try:
            for idx, spec in enumerate(articles):
                author = authors[spec['author_key']]
                category = categories[spec['category']]
                content = spec['lead'].strip()
                if spec.get('paragraphs'):
                    content += '\n\n' + '\n\n'.join(p.strip() for p in spec['paragraphs'])

                news = News(
                    title=spec['title'][:200],
                    content=content,
                    author=author,
                    status=News.Status.PUBLISHED,
                    views_count=spec.get('views_count', 120),
                    translations={},
                    video_url=spec.get('video_url', ''),
                )
                self._save_with_retry(news)

                news.categories.set([category])
                for extra in spec.get('extra_categories', []):
                    if extra in categories:
                        news.categories.add(categories[extra])

                published = timezone.now() - timedelta(hours=spec.get('hours_ago', idx + 1))
                News.all_objects.filter(pk=news.pk).update(
                    published_date=published,
                    views_count=spec.get('views_count', 120),
                )
                news.refresh_from_db()

                if not options['skip_images']:
                    self._attach_image(news, spec['category'], spec.get('image_index', idx))

                sync_news_tags(news)
                for tag_name in spec.get('tags', []):
                    tag, _ = Tag.objects.get_or_create(name=tag_name[:80])
                    news.tags.add(tag)
                index_news_document(news)
                created += 1
                if created % 10 == 0:
                    self.stdout.write(f'  … {created}/{len(articles)} articles')
        finally:
            post_save.connect(news_saved, sender=News)

        invalidate_news_caches()
        self.stdout.write(self.style.SUCCESS(f'Created {created} premium articles across {len(categories)} categories.'))

        if not options['skip_translate']:
            self.stdout.write('Running Persian translations…')
            from django.core.management import call_command
            call_command('translate_news', '--force', '--clear')

        self._print_summary(categories)
        self.stdout.write(self.style.SUCCESS('Premium seed complete.'))

    def _ensure_site_settings(self):
        obj = SiteSettings.get_solo()
        obj.site_name = 'nevox news!'
        obj.description = (
            'Independent reporting and clear analysis from around the world — '
            'breaking news, business, technology, culture, and more.'
        )
        obj.footer_text = '© nevox news!'
        obj.default_email = 'desk@nevox.news'
        obj.phone_number = '+98 21 9100 4400'
        obj.save()

    def _ensure_categories(self) -> dict[str, Category]:
        result = {}
        for name in CATEGORY_NAMES:
            cat, _ = Category.objects.get_or_create(name=name)
            result[name] = cat
        cache.delete('categories_all')
        return result

    def _ensure_authors(self) -> dict[str, CustomUser]:
        mapping = {}
        for spec in AUTHORS:
            user = CustomUser.objects.filter(username=spec['username']).first()
            if not user:
                user = CustomUser.objects.create_user(
                    username=spec['username'],
                    password='seedpass123',
                    email=spec['email'],
                    phone_number=spec['phone'],
                    user_type='admin',
                    first_name=spec['first_name'],
                    last_name=spec['last_name'],
                )
            mapping[spec['key']] = user

        admin = CustomUser.objects.filter(user_type='super_admin').first()
        if not admin:
            admin = CustomUser.objects.create_user(
                username='admin',
                password=getattr(settings, 'SEED_ADMIN_PASSWORD', None) or 'admin1234',
                email='admin@nevox.news',
                phone_number='09120000000',
                user_type='super_admin',
            )
        mapping['admin'] = admin
        return mapping

    def _save_with_retry(self, news: News, attempts: int = 5):
        import time
        from django.db.utils import OperationalError

        for attempt in range(attempts):
            try:
                news.save()
                return
            except OperationalError as exc:
                if attempt == attempts - 1:
                    raise
                connection.close()
                time.sleep(0.5 * (attempt + 1))
                self.stdout.write(self.style.WARNING(f'  DB retry {attempt + 1}: {exc}'))

    def _attach_image(self, news: News, category: str, index: int):
        url = image_url(category, index)
        try:
            data = self._fetch_bytes(url)
            ext = 'jpg'
            fname = f'{news.slug or news.pk}-{category}.{ext}'
            news.image.save(fname, ContentFile(data), save=True)
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f'  Image failed for «{news.title[:40]}…»: {exc}'))

    def _fetch_bytes(self, url: str) -> bytes:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()

    def _print_summary(self, categories: dict[str, Category]):
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('Summary'))
        for name in CATEGORY_NAMES:
            count = News.objects.filter(categories=categories[name]).distinct().count()
            self.stdout.write(f'  {name}: {count}')
        self.stdout.write(f'  TOTAL published: {News.objects.filter(status=News.Status.PUBLISHED).count()}')
        with_video = News.objects.filter(video_url__gt='').count() + News.objects.exclude(video='').count()
        with_image = News.objects.exclude(image='').count()
        self.stdout.write(f'  With images: {with_image} | With video: {with_video}')
