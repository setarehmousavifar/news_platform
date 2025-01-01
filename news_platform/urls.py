"""
URL configuration for news_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from news.views import home
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),  # مسیر صفحه اصلی
    path('news/', include('news.urls')),  # مسیر اپلیکیشن news
    path('accounts/', include('accounts.urls')),  # مسیر اپلیکیشن accounts
    path('admin/', admin.site.urls),
    path('api/', include('news.api_urls')),  # آدرس‌های API
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),  # صفحه درباره ما
    path('contact/', TemplateView.as_view(template_name="contact.html"), name='contact'),  # صفحه تماس با ما
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)