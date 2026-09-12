from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0016_tag_and_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='video_url',
            field=models.URLField(blank=True, max_length=500, verbose_name='Video URL (embed)'),
        ),
    ]
