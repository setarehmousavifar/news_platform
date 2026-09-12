from django.urls import path

from . import views

urlpatterns = [
    path('news/<int:pk>/comment/add/', views.add_comment, name='add_comment'),
    path('news/<int:news_id>/like/', views.like_news, name='like_news'),
    path('news/<int:news_id>/save/', views.toggle_save_article, name='toggle_save_article'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
