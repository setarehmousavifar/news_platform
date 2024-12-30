from django.db import models
from django.contrib.auth.models import AbstractUser


# مدل کاربر سفارشی
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="شماره موبایل")  # شماره موبایل
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")  # آیا ادمین است؟
    is_superuser = models.BooleanField(default=False, verbose_name="کاربر ارشد")  # آیا کاربر ارشد است؟

    def __str__(self):
        return self.username  # نمایش نام کاربری در ادمین پنل
