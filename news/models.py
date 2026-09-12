from django.db import models
from django.db.models import Prefetch
from django.utils.text import slugify
from django.core.cache import cache

from accounts.models import CustomUser


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')
    slug = models.SlugField(max_length=120, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Description')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'category'
            slug = base
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        cache.delete('categories_all')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name='Tag Name')
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'tag'
            slug = base
            counter = 1
            while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class News(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=200, verbose_name='Title')
    slug = models.SlugField(max_length=220, unique=True, null=True, blank=True)
    content = models.TextField(verbose_name='Content')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Published Date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Author',
    )
    categories = models.ManyToManyField(Category, verbose_name='Categories')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Keywords')
    image = models.ImageField(upload_to='news_images/', blank=True, verbose_name='Image')
    video = models.FileField(upload_to='news_videos/', blank=True, verbose_name='Video')
    video_url = models.URLField(blank=True, max_length=500, verbose_name='Video URL (embed)')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Views Count')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name='Status',
    )
    is_deleted = models.BooleanField(default=False, db_index=True)
    translations = models.JSONField(default=dict, blank=True, verbose_name='Translations')

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date'], name='news_published_idx'),
            models.Index(fields=['-views_count'], name='news_views_idx'),
            models.Index(fields=['status'], name='news_status_idx'),
            models.Index(fields=['slug'], name='news_slug_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'news'
            slug = base
            counter = 1
            while News.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.status = self.Status.ARCHIVED
        self.save(update_fields=['is_deleted', 'status', 'updated_at'])

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=['is_deleted', 'updated_at'])

    def total_likes(self):
        return self.liked_by.filter(is_like=True).count()

    def total_dislikes(self):
        return self.liked_by.filter(is_like=False).count()

    def localized_title(self, lang=None):
        from .translation_service import get_localized_field
        return get_localized_field(self, 'title', lang)

    def localized_content(self, lang=None):
        from .translation_service import get_localized_field
        return get_localized_field(self, 'content', lang)

    @property
    def video_embed_url(self):
        """YouTube/Vimeo watch or embed URL → iframe-safe embed URL."""
        import re

        url = (self.video_url or '').strip()
        if not url:
            return ''
        yt = re.search(
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})',
            url,
        )
        if yt:
            return f'https://www.youtube.com/embed/{yt.group(1)}?rel=0&modestbranding=1'
        vimeo = re.search(r'vimeo\.com/(?:video/)?(\d+)', url)
        if vimeo:
            return f'https://player.vimeo.com/video/{vimeo.group(1)}'
        if 'youtube.com/embed/' in url or 'player.vimeo.com' in url:
            return url
        return ''

    @property
    def has_video_media(self):
        return bool(self.video_embed_url or self.video)

    def __str__(self):
        return self.title


class NewsInlineImage(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='inline_images',
        verbose_name='News',
    )
    image = models.ImageField(upload_to='news_inline/', verbose_name='Image')
    caption = models.CharField(max_length=255, blank=True, verbose_name='Caption')
    order = models.PositiveSmallIntegerField(default=1, verbose_name='Order')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Inline image'
        verbose_name_plural = 'Inline images'

    def __str__(self):
        return f'Inline #{self.order} — {self.news_id}'
