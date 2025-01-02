from django.contrib import admin
from .models import CustomUser
from .models import SiteSettings

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'user_type', 'is_active')  # نمایش نوع کاربر و اطلاعات دیگر
    list_filter = ('user_type', 'is_active')  # قابلیت فیلتر بر اساس نوع کاربر
    search_fields = ('username', 'phone_number')  # قابلیت جستجو بر اساس نام کاربری و شماره موبایل
    ordering = ('-date_joined',)  # مرتب‌سازی بر اساس تاریخ عضویت


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'default_email')  # نمایش نام سایت و ایمیل پیش‌فرض
    list_editable = ('default_email',)  # امکان ویرایش سریع ایمیل پیش‌فرض
