# Generated by Django 3.2 on 2021-04-15 19:42

from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import uuid
import video.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Категория ролика',
                'verbose_name_plural': 'Категории ролика',
            },
        ),
        migrations.CreateModel(
            name='VideoAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='uuid')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('order', models.PositiveIntegerField(default=0)),
                ('type', models.CharField(choices=[('MAI', 'Основной'), ('LIS', 'Пользовательский'), ('DEL', 'Удалённый'), ('PRI', 'Приватный'), ('CLO', 'Закрытый менеджером'), ('MAN', 'Созданный персоналом'), ('PRO', 'Обработка')], default='PRO', max_length=5, verbose_name='Тип альбома')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_user_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('users', models.ManyToManyField(blank=True, related_name='users_video_album', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Видеоальбом',
                'verbose_name_plural': 'Видеоальбомы',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=video.helpers.upload_to_video_directory, verbose_name='Обложка')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Описание')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('uri', models.CharField(max_length=255, verbose_name='Ссылка на видео')),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='uuid')),
                ('status', models.CharField(choices=[('PRO', 'Обработка'), ('PUB', 'Опубликовано'), ('DEL', 'Удалено'), ('PRI', 'Приватно'), ('CLO', 'Закрыто модератором'), ('MAN', 'Созданный персоналом')], default='PRO', max_length=3)),
                ('album', models.ManyToManyField(blank=True, related_name='video_album', to='video.VideoAlbum', verbose_name='Альбом')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_category', to='video.videocategory', verbose_name='Категория')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Видео-ролики',
                'verbose_name_plural': 'Видео-ролики',
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='video',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='video_video_created_babb90_brin'),
        ),
    ]
