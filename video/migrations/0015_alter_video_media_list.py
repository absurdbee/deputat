# Generated by Django 3.2.5 on 2021-10-09 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0011_medialist_count'),
        ('video', '0014_auto_20211008_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='media_list',
            field=models.ManyToManyField(blank=True, related_name='video_media_list', to='lists.MediaList', verbose_name='Медиа-список'),
        ),
    ]