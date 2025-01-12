from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Custom Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2']  # Form fields
        labels = {
            'username': 'Username',
            'phone_number': 'Phone Number',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
