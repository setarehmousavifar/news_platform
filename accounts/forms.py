from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import SiteSettings

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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type']


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['site_name', 'footer_text']


class EditUserRoleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_type']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }
