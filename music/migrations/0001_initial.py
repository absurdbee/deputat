# Generated by Django 3.2 on 2021-04-15 19:42

from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields
import music.helpers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SoundList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('MAI', 'Основной'), ('LIS', 'Пользовательский'), ('DEL', 'Удалённый'), ('PRI', 'Приватный'), ('CLO', 'Закрытый менеджером'), ('MAN', 'Созданный персоналом'), ('PRO', 'Обработка')], default='PRO', max_length=5, verbose_name='Тип')),
                ('order', models.PositiveIntegerField(default=0)),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='uuid')),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, upload_to=music.helpers.upload_to_music_directory)),
                ('creator', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='user_playlist', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('users', models.ManyToManyField(blank=True, related_name='user_soundlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'список треков',
                'verbose_name_plural': 'списки треков',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artwork_url', imagekit.models.fields.ProcessedImageField(blank=True, upload_to=music.helpers.upload_to_music_directory)),
                ('file', models.FileField(upload_to=music.helpers.upload_to_music_directory, verbose_name='Аудиозапись')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('duration', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('PRO', 'Обработка'), ('PUB', 'Опубликовано'), ('DEL', 'Удалено'), ('PRI', 'Приватно'), ('CLO', 'Закрыто модератором'), ('MAN', 'Созданный персоналом')], default='PRO', max_length=5, verbose_name='Тип')),
                ('list', models.ManyToManyField(blank='True', related_name='playlist', to='music.SoundList')),
            ],
            options={
                'verbose_name': 'треки',
                'verbose_name_plural': 'треки',
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='music',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='music_music_created_577adb_brin'),
        ),
    ]
