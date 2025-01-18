from django.db import models
from accounts.models import CustomUser

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self): return self.name

# News Model
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Published Date")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="news", verbose_name="Author")
    likes_count = models.IntegerField(default=0, verbose_name="Likes Count")
    categories = models.ManyToManyField(Category, verbose_name="Categories")
    image = models.ImageField(upload_to='news_images/', blank=True, verbose_name="Image")
    video = models.FileField(upload_to='news_videos/', blank=True, verbose_name="Video")
    views_count = models.IntegerField(default=0, verbose_name="Views Count")

    def __str__(self): return self.title
