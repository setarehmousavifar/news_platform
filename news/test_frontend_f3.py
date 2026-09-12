from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser, SiteSettings
from news.models import News, Category


class FrontendPhase3AdminTests(TestCase):
    def setUp(self):
        SiteSettings.get_solo()
        self.client = Client()
        self.admin = CustomUser.objects.create_user(
            username='f3admin',
            password='pass12345',
            email='f3admin@ex.com',
            phone_number='09124440001',
            user_type='admin',
        )
        self.super_admin = CustomUser.objects.create_user(
            username='f3super',
            password='pass12345',
            email='f3super@ex.com',
            phone_number='09124440002',
            user_type='super_admin',
        )
        self.category = Category.objects.create(name='AdminCat', slug='admin-cat')
        self.news = News.objects.create(
            title='Admin Managed Story',
            content='Body',
            author=self.admin,
            status=News.Status.PUBLISHED,
        )
        self.draft = News.objects.create(
            title='Draft Story',
            content='Secret',
            author=self.admin,
            status=News.Status.DRAFT,
        )
        self.news.categories.add(self.category)

    def test_dashboard_shows_stats(self):
        self.client.login(username='f3admin', password='pass12345')
        res = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'stat-card')
        self.assertContains(res, 'Published')
        self.assertContains(res, 'admin-shell')

    def test_manage_news_lists_and_filters(self):
        self.client.login(username='f3admin', password='pass12345')
        res = self.client.get(reverse('manage_news'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Admin Managed Story')
        res_draft = self.client.get(reverse('manage_news') + '?status=draft')
        self.assertContains(res_draft, 'Draft Story')
        self.assertNotContains(res_draft, 'Admin Managed Story')

    def test_normal_user_blocked_from_manage_news(self):
        normal = CustomUser.objects.create_user(
            username='f3normal',
            password='pass12345',
            email='f3n@ex.com',
            phone_number='09124440003',
            user_type='normal',
        )
        self.client.login(username='f3normal', password='pass12345')
        res = self.client.get(reverse('manage_news'))
        self.assertIn(res.status_code, (302, 403))

    def test_manage_users_super_admin_only(self):
        self.client.login(username='f3admin', password='pass12345')
        res = self.client.get(reverse('manage_users'))
        self.assertIn(res.status_code, (302, 403))

        self.client.login(username='f3super', password='pass12345')
        res = self.client.get(reverse('manage_users'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Manage users')
        self.assertContains(res, 'f3admin')
