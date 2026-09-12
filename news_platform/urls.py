"""
URL configuration for news_platform project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

from accounts.views import home_view
from news.seo_views import robots_txt
from news.sitemaps import CategorySitemap, NewsSitemap, StaticViewSitemap
from news.views import health_check

sitemaps = {
    'news': NewsSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('health/', health_check, name='health_check'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
    path('admin/', admin.site.urls),
    path('api/', include('news.api_urls')),
]

urlpatterns += i18n_patterns(
    path('', home_view, name='home'),
    path('news/', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('interactions/', include('interactions.urls')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    prefix_default_language=False,
)

if getattr(settings, 'SERVE_MEDIA', settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'news_platform.views.handler403'
handler404 = 'news_platform.views.handler404'
handler500 = 'news_platform.views.handler500'
