from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),  # لیست اخبار
    path('<int:pk>/', views.news_detail, name='news_detail'),  # مسیر جزئیات خبر

    path('create/', views.create_news, name='create_news'),
    path('edit/<int:pk>/', views.edit_news, name='edit_news'),
    path('delete/<int:pk>/', views.delete_news, name='delete_news'),

]
