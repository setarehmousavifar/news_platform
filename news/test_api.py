from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import CustomUser, SiteSettings
from news.models import News, Category
from interactions.models import Comment


class APIv1Tests(TestCase):
    def setUp(self):
        SiteSettings.get_solo()
        self.client = APIClient()
        self.admin = CustomUser.objects.create_user(
            username='apiadmin',
            password='pass12345',
            email='apiadmin@ex.com',
            phone_number='09127777777',
            user_type='admin',
        )
        self.normal = CustomUser.objects.create_user(
            username='apinormal',
            password='pass12345',
            email='apinormal@ex.com',
            phone_number='09128888888',
            user_type='normal',
        )
        self.category = Category.objects.create(name='tech-api', slug='tech-api')
        self.news = News.objects.create(
            title='API News',
            content='Body for API',
            author=self.admin,
            status='published',
        )
        self.news.categories.add(self.category)

    def test_schema_and_docs(self):
        self.assertEqual(self.client.get('/api/schema/').status_code, 200)
        self.assertEqual(self.client.get('/api/docs/').status_code, 200)

    def test_filter_by_category(self):
        response = self.client.get('/api/v1/news/', {'category': 'tech-api'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    def test_search(self):
        response = self.client.get('/api/v1/news/', {'search': 'API News'})
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.json()['count'], 1)

    def test_jwt_obtain_and_create(self):
        token_res = self.client.post(
            '/api/v1/auth/jwt/',
            {'username': 'apiadmin', 'password': 'pass12345'},
            format='json',
        )
        self.assertEqual(token_res.status_code, 200)
        access = token_res.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        create_res = self.client.post(
            '/api/v1/news/',
            {'title': 'Created via JWT', 'content': 'Hello', 'categories': ['tech-api']},
            format='json',
        )
        self.assertEqual(create_res.status_code, 201)
        self.assertEqual(create_res.json()['title'], 'Created via JWT')

    def test_comment_create_requires_auth(self):
        res = self.client.post(
            '/api/v1/comments/',
            {'news': self.news.id, 'content': 'Nice'},
            format='json',
        )
        self.assertIn(res.status_code, (401, 403))

        self.client.force_authenticate(user=self.normal)
        res = self.client.post(
            '/api/v1/comments/',
            {'news': self.news.id, 'content': 'Nice'},
            format='json',
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)

    def test_like_action(self):
        self.client.force_authenticate(user=self.normal)
        res = self.client.post(f'/api/v1/news/{self.news.slug}/like/')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()['liked'])
        self.assertEqual(res.json()['total_likes'], 1)

    def test_exception_handler_shape(self):
        res = self.client.get('/api/v1/news/does-not-exist-slug/')
        self.assertEqual(res.status_code, 404)
        body = res.json()
        self.assertIn('detail', body)

    def test_comment_rejects_draft_news(self):
        draft = News.objects.create(
            title='Draft API',
            content='Secret',
            author=self.admin,
            status='draft',
        )
        self.client.force_authenticate(user=self.normal)
        res = self.client.post(
            '/api/v1/comments/',
            {'news': draft.id, 'content': 'Should fail'},
            format='json',
        )
        self.assertEqual(res.status_code, 400)

    def test_user_has_liked_and_video_fields(self):
        self.client.force_authenticate(user=self.normal)
        self.client.post(f'/api/v1/news/{self.news.slug}/like/')
        res = self.client.get(f'/api/v1/news/{self.news.slug}/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['user_has_liked'])
        self.assertIn('video', data)
        self.assertIn('author_id', data)

    def test_legacy_api_is_paginated(self):
        res = self.client.get('/api/news/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('results', res.json())
        self.assertEqual(res.get('Deprecation'), 'true')
