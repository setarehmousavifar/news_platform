from django.db import migrations


def add_fulltext(apps, schema_editor):
    if schema_editor.connection.vendor != 'mysql':
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(1)
            FROM information_schema.statistics
            WHERE table_schema = DATABASE()
              AND table_name = 'news_news'
              AND index_name = 'news_fulltext_idx'
            """
        )
        exists = cursor.fetchone()[0] > 0
        if not exists:
            cursor.execute(
                'ALTER TABLE news_news ADD FULLTEXT INDEX news_fulltext_idx (title, content)'
            )


def drop_fulltext(apps, schema_editor):
    if schema_editor.connection.vendor != 'mysql':
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(1)
            FROM information_schema.statistics
            WHERE table_schema = DATABASE()
              AND table_name = 'news_news'
              AND index_name = 'news_fulltext_idx'
            """
        )
        exists = cursor.fetchone()[0] > 0
        if exists:
            cursor.execute('ALTER TABLE news_news DROP INDEX news_fulltext_idx')


class Migration(migrations.Migration):
    """Add MySQL/MariaDB FULLTEXT index for news search performance."""

    dependencies = [
        ('news', '0012_news_is_deleted'),
    ]

    operations = [
        migrations.RunPython(add_fulltext, drop_fulltext),
    ]
