from django.db import models
from django.contrib.auth.models import AbstractUser


# مدل کاربر سفارشی# models.py
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', 'کاربر عادی'),
        ('admin', 'ادمین'),
        ('super_admin', 'کاربر ارشد'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='normal', verbose_name="نوع کاربر")  # نوع کاربر
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="شماره موبایل")  # شماره موبایل

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"  # نمایش نام کاربری و نوع کاربر




# مدل تنظیمات سایت
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, verbose_name="نام سایت")  # نام سایت
    description = models.TextField(verbose_name="توضیحات")  # توضیحات سایت

    def __str__(self):
        return self.site_name  # نمایش نام سایت
