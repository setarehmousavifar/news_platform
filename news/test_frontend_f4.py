from django.test import TestCase, Client, override_settings
from django.urls import reverse

from accounts.models import CustomUser, SiteSettings
from news.models import News, Category


class FrontendPhase4SEOTests(TestCase):
    def setUp(self):
        SiteSettings.get_solo()
        self.client = Client()
        self.author = CustomUser.objects.create_user(
            username='f4author',
            password='pass12345',
            email='f4@ex.com',
            phone_number='09125550001',
            user_type='admin',
        )
        self.category = Category.objects.create(name='SeoCat', slug='seo-cat')
        self.news = News.objects.create(
            title='SEO Ready Headline',
            content='Body content used for meta description and JSON-LD coverage in phase four.',
            author=self.author,
            status=News.Status.PUBLISHED,
        )
        self.news.categories.add(self.category)

    def test_home_has_meta_and_website_jsonld(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="description"')
        self.assertContains(res, 'property="og:title"')
        self.assertContains(res, 'application/ld+json')
        self.assertContains(res, 'WebSite')
        self.assertContains(res, 'favicon.svg')

    def test_article_has_newsarticle_jsonld_and_og(self):
        res = self.client.get(reverse('news_detail', kwargs={'slug': self.news.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'NewsArticle')
        self.assertContains(res, 'og:type" content="article"')
        self.assertContains(res, 'SEO Ready Headline')
        self.assertContains(res, 'rel="canonical"')

    def test_robots_txt(self):
        res = self.client.get('/robots.txt')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'], 'text/plain')
        body = res.content.decode()
        self.assertIn('Sitemap:', body)
        self.assertIn('Disallow: /admin/', body)

    def test_sitemap_includes_news_and_static(self):
        res = self.client.get('/sitemap.xml')
        self.assertEqual(res.status_code, 200)
        body = res.content.decode()
        self.assertIn(self.news.slug, body)
        self.assertIn('/about/', body)
        self.assertIn('/news/category/seo-cat/', body)

    def test_list_images_are_lazy(self):
        res = self.client.get(reverse('news_list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'loading="lazy"')

    def test_public_pages_do_not_load_jquery_globally(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, 'jquery-3.6.0.min.js')
        self.assertNotContains(res, 'select2.min.js')
