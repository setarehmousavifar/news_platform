from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_list_api, name='news_list_api'),
    path('news/<int:pk>/', views.news_detail_api, name='news_detail_api'),
]
