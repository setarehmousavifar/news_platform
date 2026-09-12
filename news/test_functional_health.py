from django.test import TestCase, Client, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import CustomUser, SiteSettings
from news.models import News, Category


class FunctionalHealthSweepTests(TestCase):
    def setUp(self):
        SiteSettings.get_solo()
        self.client = Client()
        self.api = APIClient()
        self.admin = CustomUser.objects.create_user(
            username='funcadmin',
            password='pass12345',
            email='funcadmin@ex.com',
            phone_number='09127770001',
            user_type='admin',
        )
        self.normal = CustomUser.objects.create_user(
            username='funcnormal',
            password='pass12345',
            email='funcnormal@ex.com',
            phone_number='09127770002',
            user_type='normal',
        )
        self.category = Category.objects.create(name='FuncCat', slug='func-cat')
        self.published = News.objects.create(
            title='Published Func',
            content='Body',
            author=self.admin,
            status=News.Status.PUBLISHED,
        )
        self.draft = News.objects.create(
            title='Draft Func',
            content='Secret',
            author=self.admin,
            status=News.Status.DRAFT,
        )
        self.published.categories.add(self.category)

    def test_invalid_category_query_does_not_500(self):
        res = self.client.get(reverse('news_list') + '?category=abc')
        self.assertEqual(res.status_code, 200)

    def test_authenticated_non_admin_gets_403_not_login_bounce(self):
        self.client.login(username='funcnormal', password='pass12345')
        res = self.client.get(reverse('manage_news'))
        self.assertEqual(res.status_code, 403)

    def test_draft_create_redirects_to_edit_not_public_404(self):
        self.client.login(username='funcadmin', password='pass12345')
        res = self.client.post(reverse('create_news'), {
            'title': 'New Draft Piece',
            'content': 'Draft body content here',
            'status': 'draft',
            'categories': [self.category.id],
        })
        self.assertEqual(res.status_code, 302)
        created = News.objects.get(title='New Draft Piece')
        self.assertEqual(created.status, News.Status.DRAFT)
        self.assertIn(f'/news/{created.pk}/edit/', res.url)

    def test_jwt_api_flow_for_list_and_like(self):
        token = self.api.post(
            '/api/v1/auth/jwt/',
            {'username': 'funcadmin', 'password': 'pass12345'},
            format='json',
        )
        self.assertEqual(token.status_code, 200)
        access = token.json()['access']
        self.api.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        listing = self.api.get('/api/v1/news/')
        self.assertEqual(listing.status_code, 200)
        self.assertIn('results', listing.json())
        like = self.api.post(f'/api/v1/news/{self.published.slug}/like/')
        self.assertEqual(like.status_code, 200)
        self.assertTrue(like.json()['liked'])

    @override_settings(DEBUG=False)
    def test_unknown_route_uses_custom_404(self):
        res = self.client.get('/totally-missing-functional-route/')
        self.assertEqual(res.status_code, 404)
        self.assertContains(res, 'Page not found', status_code=404)

    def test_comment_unauth_redirect_preserves_next(self):
        res = self.client.post(
            reverse('news_detail', kwargs={'slug': self.published.slug}),
            {'content': 'Hello from guest'},
        )
        self.assertEqual(res.status_code, 302)
        self.assertIn('/accounts/login/', res.url)
        self.assertIn('next=', res.url)
        self.assertIn(self.published.slug, res.url)
