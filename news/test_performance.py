from django.test import TestCase, Client, override_settings
from django.core.cache import cache
from django.urls import reverse

from accounts.models import CustomUser, SiteSettings
from news.models import News, Category
from news import services


class Phase6PerformanceTests(TestCase):
    def setUp(self):
        cache.clear()
        SiteSettings.get_solo()
        self.author = CustomUser.objects.create_user(
            username='perfuser',
            password='pass12345',
            email='perf@ex.com',
            phone_number='09129999999',
            user_type='admin',
        )
        self.news = News.objects.create(
            title='Fulltext searchable article',
            content='Performance and search demo content for nevox news!',
            author=self.author,
            status='published',
        )

    def test_health_reports_search_backend(self):
        response = Client().get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(data['search'], ('mysql_fulltext', 'meilisearch', 'icontains'))
        self.assertIn('cache', data)

    def test_search_finds_news(self):
        qs = services.search_news(query='Fulltext')
        self.assertTrue(qs.filter(pk=self.news.pk).exists())

    def test_view_buffer_flushes(self):
        with override_settings(VIEW_COUNT_FLUSH_EVERY=2):
            cache.clear()
            before = News.objects.get(pk=self.news.pk).views_count
            services.increment_views(self.news.pk)
            services.increment_views(self.news.pk)
            self.news.refresh_from_db()
            self.assertEqual(self.news.views_count, before + 2)

    def test_cache_invalidation_on_save(self):
        services.get_latest_news(limit=10)
        self.assertIsNotNone(cache.get('news_latest_10'))
        self.news.title = 'Updated title for cache bust'
        self.news.save()
        self.assertIsNone(cache.get('news_latest_10'))

    def test_perf_headers(self):
        response = Client().get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('X-Response-Time-ms', response)
        self.assertIn('X-DB-Query-Count', response)
