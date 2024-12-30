from django.db import models
from accounts.models import CustomUser


# مدل اخبار
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان خبر")  # تیتر خبر
    content = models.TextField(verbose_name="متن خبر")  # متن خبر
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")  # تاریخ انتشار
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="news", verbose_name="نویسنده")  # نویسنده خبر
    likes_count = models.IntegerField(default=0, verbose_name="تعداد لایک‌ها")  # تعداد لایک‌ها

    def __str__(self):
        return self.title  # نمایش عنوان خبر
