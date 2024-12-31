from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),  # لیست اخبار
    path('add/', views.add_news, name='add_news'),  # مسیر افزودن خبر
    path('<int:pk>/', views.news_detail, name='news_detail'),  # مسیر جزئیات خبر
    path('<int:news_id>/like/', views.like_news, name='like_news'),  # مسیر لایک کردن خبر
]
