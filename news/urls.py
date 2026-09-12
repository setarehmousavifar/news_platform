from django.urls import path

from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('manage/', views.manage_news, name='manage_news'),
    path('create/', views.create_news, name='create_news'),
    path('tag/<slug:tag_slug>/', views.tag_news, name='tag_news'),
    path('category/<slug:category_slug>/', views.category_news, name='category_news'),
    path('<slug:slug>/', views.news_detail, name='news_detail'),
    path('<int:pk>/edit/', views.edit_news, name='edit_news'),
    path('<int:pk>/delete/', views.delete_news, name='delete_news'),
]
