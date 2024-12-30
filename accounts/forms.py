from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# فرم ثبت‌نام سفارشی
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2']  # فیلدهای فرم
