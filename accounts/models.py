from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', 'Normal User'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='normal',
        verbose_name='User Type',
    )
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Phone Number')
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Profile photo',
    )

    def __str__(self):
        return f'{self.username} ({self.get_user_type_display()})'

    @property
    def display_name(self):
        full = self.get_full_name().strip()
        return full or self.username

    @property
    def is_publisher(self):
        return self.user_type in ('admin', 'super_admin')


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=225, verbose_name='Site Name')
    logo = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name='Logo')
    default_email = models.EmailField(null=True, blank=True, verbose_name='Default Email')
    phone_number = models.CharField(max_length=15, default='00000000000', verbose_name='Phone Number')
    footer_text = models.TextField(null=True, blank=True, verbose_name='Footer Text')
    description = models.TextField(verbose_name='Description')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('Only one SiteSettings instance is allowed.')
        result = super().save(*args, **kwargs)
        from django.core.cache import cache
        cache.delete('site_settings_solo')
        return result

    def __str__(self):
        return self.site_name

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create(
                site_name='nevox news!',
                description='Independent reporting and clear analysis from around the world.',
                footer_text='© nevox news!',
                default_email='desk@nevox.news',
                phone_number='+98 21 9100 4400',
            )
        return obj


class RoleAuditLog(models.Model):
    actor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='role_changes_made',
    )
    target = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='role_changes_received',
    )
    old_role = models.CharField(max_length=20)
    new_role = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.target_id}: {self.old_role} → {self.new_role}'
