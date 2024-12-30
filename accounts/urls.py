from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # مسیر ثبت‌نام
    path('login/', views.user_login, name='login'),  # مسیر ورود
    path('logout/', views.user_logout, name='logout'),  # مسیر خروج
]
