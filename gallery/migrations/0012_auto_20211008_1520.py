# Generated by Django 3.2.5 on 2021-10-08 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0008_medialist'),
        ('gallery', '0011_photo_media_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='media_list',
        ),
        migrations.AddField(
            model_name='photo',
            name='media_list',
            field=models.ManyToManyField(blank=True, related_name='_gallery_photo_media_list_+', to='lists.MediaList', verbose_name='Медиа-список'),
        ),
    ]
