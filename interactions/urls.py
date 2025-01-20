from django.urls import path
from . import views

urlpatterns = [
    path('news/<int:news_id>/comment/add/', views.add_comment, name='add_comment'),
    path('news/<int:news_id>/like/', views.like_news, name='like_news'),
]
