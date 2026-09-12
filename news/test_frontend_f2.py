from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser, SiteSettings
from news.models import News, Category


class FrontendPhase2Tests(TestCase):
    def setUp(self):
        SiteSettings.get_solo()
        self.client = Client()
        self.author = CustomUser.objects.create_user(
            username='f2author',
            password='pass12345',
            email='f2@ex.com',
            phone_number='09123333333',
            user_type='admin',
        )
        self.category = Category.objects.create(name='Design', slug='design')
        self.news = News.objects.create(
            title='Design System Story',
            content='Body for phase two UX coverage.',
            author=self.author,
            status=News.Status.PUBLISHED,
        )
        self.news.categories.add(self.category)

    def test_design_system_assets_linked(self):
        res = self.client.get(reverse('home'))
        self.assertContains(res, 'css/style.css')
        self.assertContains(res, 'Fraunces')
        self.assertContains(res, 'Manrope')
        self.assertContains(res, 'site-nav')

    def test_login_has_visible_labels(self):
        res = self.client.get(reverse('login'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Username')
        self.assertContains(res, 'Password')
        self.assertContains(res, 'auth-panel')

    def test_news_list_uses_story_tiles(self):
        res = self.client.get(reverse('news_list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'story-grid')
        self.assertContains(res, 'story-tile')

    def test_about_and_contact_use_site_settings(self):
        about = self.client.get(reverse('about'))
        contact = self.client.get(reverse('contact'))
        self.assertEqual(about.status_code, 200)
        self.assertEqual(contact.status_code, 200)
        self.assertContains(about, 'About')
        self.assertContains(contact, 'Contact')
