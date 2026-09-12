from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import profile_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('check-username/', views.check_username, name='check_username'),
    path('profile/', profile_view, name='profile'),
    path('saved/', views.saved_stories, name='saved_stories'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('manage_users/', views.manage_users, name='manage_users'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('edit_user_role/<int:user_id>/', views.edit_user_role, name='edit_user_role'),

    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
