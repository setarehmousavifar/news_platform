from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser
from news.models import News
from interactions.models import Comment
from interactions.services import toggle_news_like


class InteractionsServiceTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='liker',
            password='pass12345',
            email='liker@example.com',
            phone_number='09124444444',
        )
        self.news = News.objects.create(
            title='Like me',
            content='Body',
            author=self.user,
            status=News.Status.PUBLISHED,
        )

    def test_like_toggle_idempotent_cycle(self):
        liked, total = toggle_news_like(self.user, self.news)
        self.assertTrue(liked)
        self.assertEqual(total, 1)
        liked, total = toggle_news_like(self.user, self.news)
        self.assertFalse(liked)
        self.assertEqual(total, 0)


class InteractionsViewHardeningTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='viewer',
            password='pass12345',
            email='viewer@example.com',
            phone_number='09125555555',
        )
        self.draft = News.objects.create(
            title='Draft',
            content='Hidden',
            author=self.user,
            status=News.Status.DRAFT,
        )

    def test_cannot_like_draft_news(self):
        self.client.login(username='viewer', password='pass12345')
        res = self.client.post(reverse('like_news', args=[self.draft.id]))
        self.assertEqual(res.status_code, 404)

    def test_anonymous_like_returns_json_401(self):
        published = News.objects.create(
            title='Pub',
            content='Body',
            author=self.user,
            status=News.Status.PUBLISHED,
        )
        res = self.client.post(reverse('like_news', args=[published.id]))
        self.assertEqual(res.status_code, 401)
        self.assertIn('login_url', res.json())
