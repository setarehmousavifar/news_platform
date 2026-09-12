from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser, SiteSettings, RoleAuditLog
from accounts.permissions import can_edit_news, can_manage_user, can_assign_role
from accounts.services import change_user_role
from news.models import News, Category


class RoleMatrixTests(TestCase):
    def setUp(self):
        SiteSettings.get_solo()
        self.super_admin = CustomUser.objects.create_user(
            username='sa', password='pass12345', email='sa@ex.com',
            phone_number='09120000001', user_type='super_admin',
        )
        self.admin = CustomUser.objects.create_user(
            username='ad', password='pass12345', email='ad@ex.com',
            phone_number='09120000002', user_type='admin',
        )
        self.admin2 = CustomUser.objects.create_user(
            username='ad2', password='pass12345', email='ad2@ex.com',
            phone_number='09120000003', user_type='admin',
        )
        self.normal = CustomUser.objects.create_user(
            username='nu', password='pass12345', email='nu@ex.com',
            phone_number='09120000004', user_type='normal',
        )
        for u in (self.super_admin, self.admin, self.admin2, self.normal):
            u.refresh_from_db()

        self.category = Category.objects.create(name='technology')
        self.news = News.objects.create(
            title='Owned by admin', content='body', author=self.admin, status='published',
        )
        self.news.categories.add(self.category)

    def test_staff_flags_synced(self):
        self.assertTrue(self.super_admin.is_staff and self.super_admin.is_superuser)
        self.assertTrue(self.admin.is_staff and not self.admin.is_superuser)
        self.assertFalse(self.normal.is_staff)

    def test_object_permissions(self):
        self.assertTrue(can_edit_news(self.super_admin, self.news))
        self.assertTrue(can_edit_news(self.admin, self.news))
        self.assertFalse(can_edit_news(self.admin2, self.news))
        self.assertFalse(can_edit_news(self.normal, self.news))

    def test_cannot_manage_self(self):
        self.assertFalse(can_manage_user(self.super_admin, self.super_admin))
        self.assertTrue(can_manage_user(self.super_admin, self.admin))

    def test_role_change_audited(self):
        change_user_role(actor=self.super_admin, target=self.normal, new_role='admin')
        self.normal.refresh_from_db()
        self.assertEqual(self.normal.user_type, 'admin')
        self.assertTrue(self.normal.is_staff)
        self.assertEqual(RoleAuditLog.objects.count(), 1)

    def test_create_news_forbidden_for_normal(self):
        client = Client()
        client.login(username='nu', password='pass12345')
        response = client.get(reverse('create_news'))
        self.assertEqual(response.status_code, 403)

    def test_api_v1_list_public(self):
        client = Client()
        response = client.get('/api/v1/news/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())

    def test_api_v1_create_requires_admin(self):
        client = Client()
        response = client.post('/api/v1/news/', {'title': 'X', 'content': 'Y'}, content_type='application/json')
        self.assertIn(response.status_code, (401, 403))

    def test_slug_detail_page(self):
        client = Client()
        response = client.get(reverse('news_detail', kwargs={'slug': self.news.slug}))
        self.assertEqual(response.status_code, 200)

    def test_assign_role_only_super_admin(self):
        self.assertTrue(can_assign_role(self.super_admin, 'admin'))
        self.assertFalse(can_assign_role(self.admin, 'super_admin'))

    def test_logout_requires_post(self):
        client = Client()
        client.login(username='nu', password='pass12345')
        get_res = client.get(reverse('logout'))
        self.assertEqual(get_res.status_code, 405)
        post_res = client.post(reverse('logout'))
        self.assertEqual(post_res.status_code, 302)
