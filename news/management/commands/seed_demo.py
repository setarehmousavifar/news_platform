from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import CustomUser, SiteSettings
from news.models import Category, News


class Command(BaseCommand):
    help = 'Seed demo categories, site settings, and sample news for local development.'

    def handle(self, *args, **options):
        settings_obj = SiteSettings.get_solo()
        settings_obj.site_name = 'nevox news!'
        settings_obj.description = (
            settings_obj.description
            or 'Independent reporting and clear analysis from around the world.'
        )
        settings_obj.footer_text = '© nevox news!'
        settings_obj.default_email = settings_obj.default_email or 'desk@nevox.news'
        if not settings_obj.phone_number or settings_obj.phone_number == '00000000000':
            settings_obj.phone_number = '+98 21 9100 4400'
        settings_obj.save()
        self.stdout.write(self.style.SUCCESS('SiteSettings ready'))

        categories = []
        category_names = [
            'breaking_news', 'world', 'politics', 'business', 'economy', 'technology',
            'science', 'health', 'sports', 'entertainment', 'culture', 'lifestyle',
            'opinion', 'education', 'environment', 'crime', 'travel', 'food',
            'real_estate', 'weather', 'video',
        ]
        Category.objects.filter(name='auto').delete()
        from django.core.cache import cache
        cache.delete('categories_all')
        for name in category_names:
            cat, _ = Category.objects.get_or_create(name=name)
            cat.save()
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS(f'Categories: {len(categories)}'))

        admin_user = CustomUser.objects.filter(user_type='super_admin').first()
        if not admin_user:
            password = getattr(settings, 'SEED_ADMIN_PASSWORD', None) or 'admin1234'
            if password == 'admin1234':
                self.stdout.write(self.style.WARNING(
                    'Using default seed password admin1234. '
                    'Set SEED_ADMIN_PASSWORD in .env for stronger local demos.'
                ))
            admin_user = CustomUser.objects.create_user(
                username='admin',
                password=password,
                email='admin@nevox.news',
                phone_number='09120000000',
                user_type='super_admin',
            )
            self.stdout.write(self.style.WARNING(f'Created admin (password from SEED_ADMIN_PASSWORD or default)'))

        if not News.objects.filter(slug='welcome-to-nevox-news').exists():
            news = News.objects.create(
                title='Welcome to nevox news!',
                content=(
                    'This is a starter article for local development. '
                    'Use seed_premium for a full demo dataset with categories, images, and sample authors.'
                ),
                author=admin_user,
                status=News.Status.PUBLISHED,
            )
            if categories:
                news.categories.add(categories[0])
            self.stdout.write(self.style.SUCCESS(f'Sample news: /news/{news.slug}/'))
        else:
            self.stdout.write('Sample news already exists')

        self.stdout.write(self.style.SUCCESS('Seed complete.'))
