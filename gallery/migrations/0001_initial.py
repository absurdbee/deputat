# Generated by Django 3.2 on 2021-04-15 19:42

from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import gallery.helpers
import imagekit.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='uuid')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('type', models.CharField(choices=[('MAI', 'Фото со стены'), ('LIS', 'Пользовательский'), ('DEL', 'Удалённый'), ('PRI', 'Приватный'), ('CLO', 'Закрытый менеджером'), ('MAN', 'Созданный персоналом'), ('PRO', 'Обработка')], default='PRO', max_length=5, verbose_name='Тип альбома')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Фотоальбом',
                'verbose_name_plural': 'Фотоальбомы',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='uuid')),
                ('file', imagekit.models.fields.ProcessedImageField(upload_to=gallery.helpers.upload_to_photo_directory)),
                ('preview', imagekit.models.fields.ProcessedImageField(upload_to=gallery.helpers.upload_to_photo_directory)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('status', models.CharField(choices=[('PRO', 'Обработка'), ('PUB', 'Опубликовано'), ('DEL', 'Удалено'), ('PRI', 'Приватно'), ('CLO', 'Закрыто модератором'), ('MAN', 'Созданный персоналом')], default='PRO', max_length=5, verbose_name='Тип альбома')),
                ('album', models.ManyToManyField(blank=True, related_name='photo_album', to='gallery.Album')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фото',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='album',
            name='cover_photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='gallery.photo', verbose_name='Обожка'),
        ),
        migrations.AddField(
            model_name='album',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_album_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
        migrations.AddField(
            model_name='album',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='users_photolist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='photo',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='gallery_pho_created_389e41_brin'),
        ),
        migrations.AddIndex(
            model_name='album',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='gallery_alb_created_8f2540_brin'),
        ),
    ]