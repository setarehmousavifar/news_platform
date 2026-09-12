import re
import uuid

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator

from .models import CustomUser, SiteSettings
from .permissions import can_assign_role, can_manage_user, ROLE_NORMAL

AUTH_INPUT_CLASS = 'form-control'
AUTH_INVALID_CLASS = 'is-invalid'
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9]+$')


def _auth_widget(placeholder=''):
    attrs = {'class': AUTH_INPUT_CLASS}
    if placeholder:
        attrs['placeholder'] = placeholder
    return attrs


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs=_auth_widget('First name')),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs=_auth_widget('Last name')),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs=_auth_widget('you@example.com')),
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
            'username': 'Username',
            'password1': 'Password',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                **_auth_widget('Letters and numbers only'),
                'pattern': '[A-Za-z0-9]+',
                'autocomplete': 'username',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control password-field__input',
                'placeholder': 'At least 8 characters',
                'autocomplete': 'new-password',
                'data-password-toggle': 'true',
                'minlength': '8',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2', None)
        required_fields = ('first_name', 'last_name', 'username', 'email', 'password1')
        for name in required_fields:
            if name in self.fields:
                self.fields[name].required = True
        if 'first_name' in self.fields:
            self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['username'].validators = [
            MinLengthValidator(3, message='Username must be at least 3 characters.'),
            RegexValidator(
                r'^[a-zA-Z0-9]+$',
                message='Username can only contain letters and numbers.',
            ),
        ]
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control password-field__input',
            'autocomplete': 'new-password',
            'data-password-toggle': 'true',
            'minlength': '8',
        })

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            password_validation.validate_password(password, self.instance)
        return password

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError('This email is already registered. Try logging in or use a different email.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if not USERNAME_PATTERN.match(username):
            raise ValidationError('Username can only contain letters and numbers.')
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken. Please choose another one.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = ROLE_NORMAL
        user.email = self.cleaned_data['email'].strip().lower()
        phone = (self.cleaned_data.get('phone_number') or '').strip()
        if not phone:
            phone = f'np{uuid.uuid4().hex[:11]}'
        user.phone_number = phone
        if commit:
            user.save()
        return user


class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Username',
        widget=forms.TextInput(attrs=_auth_widget('Your username')),
    )
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs=_auth_widget('you@example.com')),
    )

    def get_matching_user(self):
        username = self.cleaned_data.get('username', '').strip()
        email = self.cleaned_data.get('email', '').strip().lower()
        if not username or not email:
            return None
        return CustomUser.objects.filter(username__iexact=username, email__iexact=email).first()

    def send_reset_email(self, request):
        user = self.get_matching_user()
        if not user:
            return False
        form = PasswordResetForm({'email': user.email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
            )
            return True
        return False


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs=_auth_widget('First name')),
            'last_name': forms.TextInput(attrs=_auth_widget('Last name')),
            'username': forms.TextInput(attrs=_auth_widget('Username')),
            'email': forms.EmailInput(attrs=_auth_widget('you@example.com')),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'first_name' in self.fields:
            self.fields['first_name'].widget.attrs['autofocus'] = True
        if 'username' in self.fields:
            self.fields['username'].help_text = ''
        if not getattr(self.instance, 'is_publisher', False):
            self.fields.pop('avatar', None)

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = CustomUser.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('This email is already in use.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if not USERNAME_PATTERN.match(username):
            raise ValidationError('Username can only contain letters and numbers.')
        qs = CustomUser.objects.filter(username__iexact=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('This username is already taken.')
        return username


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type']

    def __init__(self, *args, actor=None, **kwargs):
        self.actor = actor
        super().__init__(*args, **kwargs)

    def clean_user_type(self):
        new_role = self.cleaned_data['user_type']
        if self.actor and not can_assign_role(self.actor, new_role):
            raise ValidationError('You are not allowed to assign this role.')
        if self.actor and self.instance.pk == self.actor.pk:
            raise ValidationError('You cannot change your own role here.')
        return new_role


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

    def __init__(self, *args, actor=None, **kwargs):
        self.actor = actor
        super().__init__(*args, **kwargs)

    def clean_user_type(self):
        new_role = self.cleaned_data['user_type']
        if self.actor and not can_assign_role(self.actor, new_role):
            raise ValidationError('You are not allowed to assign this role.')
        if self.actor and self.instance.pk == self.actor.pk:
            raise ValidationError('You cannot change your own role.')
        if self.actor and not can_manage_user(self.actor, self.instance):
            raise ValidationError('You cannot manage this user.')
        return new_role
