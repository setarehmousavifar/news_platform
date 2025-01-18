from django.contrib import admin
from .models import News, Category

# ثبت مدل اخبار
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_categories', 'published_date')  # ستون‌هایی که در لیست نمایش داده می‌شوند
    search_fields = ('title', 'content')  # قابلیت جستجو بر اساس این فیلدها
    list_filter = ('author',)  # فقط فیلترهایی که روی فیلدهای عادی قابل اجرا هستند

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])  # تبدیل به رشته
    get_categories.short_description = 'Categories'  # عنوان ستون در ادمین

# ثبت مدل دسته‌بندی
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # ستون‌های نمایش داده شده
