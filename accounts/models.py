from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (('normal', 'Normal User'), ('admin', 'Admin'), ('super_admin', 'Super Admin'))
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='normal', verbose_name="User Type")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number")
    email = models.EmailField(unique=True)
    
    def __str__(self): return f"{self.username} ({self.get_user_type_display()})"

# Site Settings Model
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=225, verbose_name="Site Name")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name="Logo")
    default_email = models.EmailField(null=True, blank=True, verbose_name="Default Email")
    phone_number = models.CharField(max_length=15, default='00000000000', verbose_name="Phone Number")
    footer_text = models.TextField(null=True, blank=True, verbose_name="Footer Text")
    description = models.TextField(verbose_name="Description")

    def __str__(self): return self.site_name
