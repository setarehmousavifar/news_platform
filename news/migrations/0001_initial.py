# Generated by Django 5.1.4 on 2024-12-30 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان خبر')),
                ('content', models.TextField(verbose_name='متن خبر')),
                ('published_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')),
                ('likes_count', models.IntegerField(default=0, verbose_name='تعداد لایک\u200cها')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
        ),
    ]
