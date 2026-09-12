from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser, SiteSettings
from news.models import News, Category


class FrontendPhase5A11yAndRoleQATests(TestCase):
    def setUp(self):
        SiteSettings.get_solo()
        self.client = Client()
        self.normal = CustomUser.objects.create_user(
            username='f5normal',
            password='pass12345',
            email='f5n@ex.com',
            phone_number='09126660001',
            user_type='normal',
        )
        self.admin = CustomUser.objects.create_user(
            username='f5admin',
            password='pass12345',
            email='f5a@ex.com',
            phone_number='09126660002',
            user_type='admin',
        )
        self.super_admin = CustomUser.objects.create_user(
            username='f5super',
            password='pass12345',
            email='f5s@ex.com',
            phone_number='09126660003',
            user_type='super_admin',
        )
        self.category = Category.objects.create(name='QACat', slug='qa-cat')
        self.news = News.objects.create(
            title='QA Published Story',
            content='Accessible article body for defense QA coverage.',
            author=self.admin,
            status=News.Status.PUBLISHED,
        )
        self.other = News.objects.create(
            title='Other Author Story',
            content='Belongs to super admin.',
            author=self.super_admin,
            status=News.Status.PUBLISHED,
        )
        self.news.categories.add(self.category)

    def test_skip_link_and_main_landmark(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'skip-link')
        self.assertContains(res, 'href="#main-content"')
        self.assertContains(res, 'id="main-content"')
        self.assertContains(res, 'aria-label="Primary"')

    def test_theme_toggle_has_pressed_state(self):
        res = self.client.get(reverse('home'))
        self.assertContains(res, 'id="theme-toggle"')
        self.assertContains(res, 'aria-pressed')

    def test_login_labels_and_autocomplete(self):
        res = self.client.get(reverse('login'))
        self.assertContains(res, 'for="username"')
        self.assertContains(res, 'autocomplete="username"')
        self.assertContains(res, 'autocomplete="current-password"')

    def test_normal_can_read_and_is_blocked_from_admin(self):
        self.client.login(username='f5normal', password='pass12345')
        detail = self.client.get(reverse('news_detail', kwargs={'slug': self.news.slug}))
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, 'like-button')

        create = self.client.get(reverse('create_news'))
        self.assertIn(create.status_code, (302, 403))
        manage = self.client.get(reverse('manage_news'))
        self.assertIn(manage.status_code, (302, 403))
        dash = self.client.get(reverse('admin_dashboard'))
        self.assertIn(dash.status_code, (302, 403))

    def test_admin_dashboard_and_cannot_see_others_in_manage(self):
        self.client.login(username='f5admin', password='pass12345')
        dash = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(dash.status_code, 200)
        self.assertContains(dash, 'stat-card')

        manage = self.client.get(reverse('manage_news'))
        self.assertEqual(manage.status_code, 200)
        self.assertContains(manage, 'QA Published Story')
        self.assertNotContains(manage, 'Other Author Story')

        users = self.client.get(reverse('manage_users'))
        self.assertIn(users.status_code, (302, 403))

    def test_super_admin_sees_all_news_and_users(self):
        self.client.login(username='f5super', password='pass12345')
        manage = self.client.get(reverse('manage_news'))
        self.assertEqual(manage.status_code, 200)
        self.assertContains(manage, 'QA Published Story')
        self.assertContains(manage, 'Other Author Story')

        users = self.client.get(reverse('manage_users'))
        self.assertEqual(users.status_code, 200)
        self.assertContains(users, 'f5normal')
        self.assertContains(users, 'admin-shell')

    def test_reply_controls_expose_aria(self):
        self.client.login(username='f5normal', password='pass12345')
        from interactions.models import Comment
        Comment.objects.create(user=self.admin, news=self.news, content='Root comment here')
        res = self.client.get(reverse('news_detail', kwargs={'slug': self.news.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'aria-expanded="false"')
        self.assertContains(res, 'data-reply-target')
        self.assertContains(res, 'hidden')

    def test_profile_page_has_labels(self):
        self.client.login(username='f5normal', password='pass12345')
        res = self.client.get(reverse('profile'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Your profile')
        self.assertContains(res, 'for="id_email"')
        self.assertNotContains(res, 'Phone number')
