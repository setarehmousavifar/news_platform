from django.test import TestCase, Client, override_settings
from django.urls import reverse

from accounts.models import CustomUser, SiteSettings
from news.models import News, Category


class FrontendPhase1Tests(TestCase):
    def setUp(self):
        SiteSettings.get_solo()
        self.client = Client()
        self.admin = CustomUser.objects.create_user(
            username='f1admin',
            password='pass12345',
            email='f1admin@ex.com',
            phone_number='09121111111',
            user_type='admin',
        )
        self.category = Category.objects.create(name='FrontCat', slug='front-cat')
        self.news = News.objects.create(
            title='Frontend Phase One',
            content='Body content for list and detail',
            author=self.admin,
            status=News.Status.PUBLISHED,
        )
        self.news.categories.add(self.category)

    def test_news_list_preserves_query_params(self):
        url = reverse('news_list') + '?q=Frontend&category=%s&sort=popular&page=1' % self.category.id
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'sort=popular')
        self.assertContains(res, f'category={self.category.id}')
        self.assertContains(res, 'q=Frontend')
        self.assertContains(res, 'images/default_news_image.jpg')

    def test_news_detail_like_login_cta_for_anon(self):
        res = self.client.get(reverse('news_detail', kwargs={'slug': self.news.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Log in to like')
        self.assertContains(res, 'like-count')

    def test_create_form_includes_status_and_video(self):
        self.client.login(username='f1admin', password='pass12345')
        res = self.client.get(reverse('create_news'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="status"')
        self.assertContains(res, 'name="video"')
        self.assertContains(res, 'preview-btn')

    def test_navbar_uses_category_slugs_from_db(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, '/news/category/front-cat/')

    def test_home_hero_shows_brand(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'hero__brand')
        self.assertContains(res, 'hero__headline')
        self.assertContains(res, 'home-latest')

    @override_settings(DEBUG=False)
    def test_custom_404_page(self):
        res = self.client.get('/this-path-does-not-exist-f1/')
        self.assertEqual(res.status_code, 404)
        self.assertContains(res, 'Page not found', status_code=404)

    def test_legacy_add_comment_redirects_to_detail(self):
        res = self.client.get(reverse('add_comment', args=[self.news.id]))
        self.assertEqual(res.status_code, 302)
        self.assertIn(self.news.slug, res.url)
