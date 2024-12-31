from django.db import models
from accounts.models import CustomUser


# مدل دسته‌بندی برای مدیریت انواع اخبار
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")  # نام دسته‌بندی
    description = models.TextField(blank=True, verbose_name="توضیحات")  # توضیحات دسته‌بندی (اختیاری)

    def __str__(self):
        return self.name  # نمایش نام دسته‌بندی در پنل ادمین


# مدل اخبار
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان خبر")  # تیتر خبر
    content = models.TextField(verbose_name="متن خبر")  # متن خبر
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")  # تاریخ انتشار
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="news", verbose_name="نویسنده")  # نویسنده خبر
    likes_count = models.IntegerField(default=0, verbose_name="تعداد لایک‌ها")  # تعداد لایک‌ها
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="دسته‌بندی")  # ارتباط با دسته‌بندی
    image = models.ImageField(upload_to='news_images/', blank=True, verbose_name="تصویر خبر")  # آپلود تصویر خبر
    video = models.FileField(upload_to='news_videos/', blank=True, verbose_name="ویدئو خبر")


    def __str__(self):
        return self.title  # نمایش عنوان خبر


