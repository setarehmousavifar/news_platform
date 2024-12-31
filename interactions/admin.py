from django.contrib import admin
from .models import Comment, Like, CommentLike

# ثبت مدل نظرات
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'content', 'created_at')  # ستون‌های نمایش داده شده
    search_fields = ('content',)  # جستجو بر اساس متن نظر

# ثبت مدل لایک‌ها
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('news', 'user')  # ستون‌های نمایش داده شده

# ثبت مدل لایک نظرات
@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user')  # ستون‌های نمایش داده شده
