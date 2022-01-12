# Generated by Django 3.2.5 on 2021-10-02 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0008_medialist'),
        ('music', '0012_remove_music_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='media_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='lists.medialist', verbose_name='Медиа-список'),
        ),
        migrations.AlterField(
            model_name='music',
            name='list',
            field=models.ManyToManyField(blank=True, related_name='playlist', to='music.SoundList'),
        ),
    ]
