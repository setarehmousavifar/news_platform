from django.core.management.base import BaseCommand

from news.models import News
from news.services import get_meili_client, index_news_document
from django.conf import settings


class Command(BaseCommand):
    help = 'Rebuild Meilisearch news index (no-op if MEILI_URL is not configured).'

    def handle(self, *args, **options):
        client = get_meili_client()
        if client is None:
            self.stdout.write(self.style.WARNING(
                'MEILI_URL not set or meilisearch package unavailable. '
                'Using MySQL FULLTEXT / icontains instead. Nothing to rebuild.'
            ))
            return

        index_name = settings.MEILI_NEWS_INDEX
        try:
            client.create_index(index_name, {'primaryKey': 'id'})
        except Exception:
            pass

        index = client.index(index_name)
        try:
            index.update_searchable_attributes(['title', 'content', 'slug'])
        except Exception:
            pass

        docs = []
        for news in News.objects.filter(status=News.Status.PUBLISHED):
            docs.append({
                'id': news.id,
                'title': news.title,
                'content': news.content,
                'slug': news.slug or '',
                'status': news.status,
            })
            index_news_document(news)

        self.stdout.write(self.style.SUCCESS(
            f'Indexed {len(docs)} published news documents into "{index_name}".'
        ))
