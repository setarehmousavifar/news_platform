from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from news.models import News, Category


class NewsSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.8
    protocol = None  # inherit request scheme when available

    def items(self):
        return (
            News.objects.filter(status=News.Status.PUBLISHED)
            .order_by('-updated_at')
        )

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('news_detail', kwargs={'slug': obj.slug})


class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.6

    def items(self):
        return Category.objects.all().order_by('name')

    def location(self, obj):
        return reverse('category_news', kwargs={'category_slug': obj.slug})


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return ['home', 'news_list', 'about', 'contact']

    def location(self, item):
        return reverse(item)
