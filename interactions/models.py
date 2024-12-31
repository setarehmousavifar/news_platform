from django.db import models
from accounts.models import CustomUser
from news.models import News


# مدل نظرات
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments", verbose_name="کاربر")  # کاربر
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments", verbose_name="خبر")  # خبر
    content = models.TextField(verbose_name="متن نظر")  # متن نظر
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ نظر")  # زمان ایجاد نظر

    def __str__(self):
        return f"{self.user.username} - {self.news.title}"  # نمایش کاربر و خبر

# مدل لایک‌ها
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes", verbose_name="کاربر")  # کاربر
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="likes", verbose_name="خبر")  # خبر

    class Meta:
        unique_together = ('user', 'news')  # هر کاربر فقط یک بار می‌تونه یک خبر رو لایک کنه

    def __str__(self):
        return f"{self.user.username} لایک کرد {self.news.title}"  # نمایش لایک


# مدل لایک برای نظرات
class CommentLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="کاربر")  # کاربر لایک‌کننده
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="نظر")  # نظر لایک‌شده
    is_like = models.BooleanField(default=True)  # True برای لایک، False برای دیسلایک

    class Meta:
        unique_together = ('user', 'comment')  # هر کاربر فقط یک بار می‌تونه یک نظر رو لایک کنه

    def __str__(self):
        return f"{self.user.username} لایک کرد نظر {self.comment.id}"  # نمایش کاربر و نظر
