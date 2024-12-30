from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),  # لیست اخبار
    path('add/', views.add_news, name='add_news'),  # مسیر افزودن خبر
]

