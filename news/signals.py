from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import logging

from .models import News, Category
from .services import invalidate_news_caches, index_news_document, remove_news_document

logger = logging.getLogger(__name__)


@receiver(post_save, sender=News)
def news_saved(sender, instance, created, update_fields=None, **kwargs):
    skip_fields = {'translations', 'views_count', 'updated_at'}
    if update_fields is not None and set(update_fields) <= skip_fields:
        return

    invalidate_news_caches()
    if not instance.is_deleted and instance.status == News.Status.PUBLISHED:
        index_news_document(instance)
        if created or update_fields is None or {'title', 'content', 'status'} & set(update_fields or []):
            try:
                from .translation_service import ensure_news_translations
                ensure_news_translations(instance)
            except Exception:
                logger.exception('Auto-translation failed for news %s', instance.pk)
        try:
            from .tagging import sync_news_tags
            sync_news_tags(instance)
        except Exception:
            logger.exception('Auto-tagging failed for news %s', instance.pk)
    else:
        remove_news_document(instance.pk)


@receiver(post_delete, sender=News)
def news_deleted(sender, instance, **kwargs):
    invalidate_news_caches()
    remove_news_document(instance.pk)


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def category_changed(sender, **kwargs):
    invalidate_news_caches()
