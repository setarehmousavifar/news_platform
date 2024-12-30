from django.db import models
from django.contrib.auth.models import AbstractUser


# مدل کاربر سفارشی
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="شماره موبایل")  # شماره موبایل
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")  # آیا ادمین است؟
    is_superuser = models.BooleanField(default=False, verbose_name="کاربر ارشد")  # آیا کاربر ارشد است؟

    def __str__(self):
        return self.username  # نمایش نام کاربری در ادمین پنل


# مدل تنظیمات سایت
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, verbose_name="نام سایت")  # نام سایت
    description = models.TextField(verbose_name="توضیحات")  # توضیحات سایت

    def __str__(self):
        return self.site_name  # نمایش نام سایت
