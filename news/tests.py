from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache

from accounts.models import CustomUser, SiteSettings
from news.models import News, Category
from news import services
from interactions.services import toggle_comment_like
from interactions.models import Comment


class SoftDeleteAndCacheTests(TestCase):
    def setUp(self):
        cache.clear()
        SiteSettings.get_solo()
        self.author = CustomUser.objects.create_user(
            username='author4', password='pass12345', email='a4@ex.com',
            phone_number='09125555555', user_type='admin',
        )
        self.news = News.objects.create(
            title='Soft Delete Me', content='body', author=self.author, status='published',
        )

    def test_soft_delete_hides_from_default_manager(self):
        services.soft_delete_news(self.news)
        self.assertFalse(News.objects.filter(pk=self.news.pk).exists())
        self.assertTrue(News.all_objects.filter(pk=self.news.pk, is_deleted=True).exists())

    def test_health_endpoint(self):
        response = Client().get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_categories_cached(self):
        Category.objects.create(name='cache-cat')
        first = services.list_categories()
        second = services.list_categories()
        self.assertEqual(len(first), len(second))

    def test_comment_like_toggle(self):
        comment = Comment.objects.create(user=self.author, news=self.news, content='hi')
        result = toggle_comment_like(self.author, comment, is_like=True)
        self.assertTrue(result['liked'])
        self.assertEqual(result['total_likes'], 1)
        result = toggle_comment_like(self.author, comment, is_like=True)
        self.assertTrue(result['removed'])
        self.assertEqual(result['total_likes'], 0)


class NewsListCBVTests(TestCase):
    def setUp(self):
        SiteSettings.get_solo()
        self.author = CustomUser.objects.create_user(
            username='listauthor', password='pass12345', email='la@ex.com',
            phone_number='09126666666', user_type='admin',
        )
        News.objects.create(title='Listed', content='c', author=self.author, status='published')

    def test_list_view(self):
        response = Client().get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Listed')
