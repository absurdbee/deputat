# Generated by Django 2.2.16 on 2020-11-11 14:07

from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import users.helpers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20201111_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', imagekit.models.fields.ProcessedImageField(upload_to=users.helpers.upload_to_user_directory)),
                ('preview', imagekit.models.fields.ProcessedImageField(upload_to=users.helpers.upload_to_user_directory)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('post', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blog.ElectNew')),
            ],
            options={
                'verbose_name_plural': 'Фото',
                'verbose_name': 'Фото',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ElectDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('file', models.FileField(upload_to=users.helpers.upload_to_user_directory, verbose_name='Документ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('post', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blog.ElectNew')),
            ],
            options={
                'verbose_name_plural': 'Документы',
                'verbose_name': 'Документ',
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='electphoto',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='blog_electp_created_c29d89_brin'),
        ),
        migrations.AddIndex(
            model_name='electdoc',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='blog_electd_created_35020a_brin'),
        ),
    ]
