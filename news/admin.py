from django.contrib import admin
from .models import News, Category

# ثبت مدل اخبار
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published_date')  # ستون‌هایی که در لیست نمایش داده می‌شوند
    search_fields = ('title', 'content')  # قابلیت جستجو بر اساس این فیلدها
    list_filter = ('category', 'author')  # قابلیت فیلتر کردن بر اساس این فیلدها

# ثبت مدل دسته‌بندی
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # ستون‌های نمایش داده شده
