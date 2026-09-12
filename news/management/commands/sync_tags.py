from django.core.management.base import BaseCommand

from news.models import News
from news.tagging import sync_news_tags


class Command(BaseCommand):
    help = 'Generate or refresh keyword tags for published news.'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, help='Sync tags for a single news item by ID')

    def handle(self, *args, **options):
        qs = News.objects.filter(status=News.Status.PUBLISHED, is_deleted=False).prefetch_related('categories')
        if options['id']:
            qs = qs.filter(pk=options['id'])
        total = qs.count()
        self.stdout.write(f'Syncing tags for {total} stories…')
        for i, news in enumerate(qs.iterator(), 1):
            tags = sync_news_tags(news)
            self.stdout.write(f'  [{i}/{total}] {news.pk}: {", ".join(t.name for t in tags)}')
        self.stdout.write(self.style.SUCCESS('Done.'))
