from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Custom Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2']  # Form fields
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'username': 'Username',
            'phone_number': 'Phone Number',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
