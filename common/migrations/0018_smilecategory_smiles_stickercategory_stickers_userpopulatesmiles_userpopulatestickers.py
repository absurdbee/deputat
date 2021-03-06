# Generated by Django 3.2.5 on 2021-12-26 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0017_auto_20211118_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmileCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Название')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядковый номер')),
            ],
            options={
                'verbose_name': 'Категория смайликов',
                'verbose_name_plural': 'Категории смайликов',
            },
        ),
        migrations.CreateModel(
            name='Smiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Название')),
                ('image', models.ImageField(upload_to='smiles/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='common.smilecategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Смайл',
                'verbose_name_plural': 'Смайлы',
            },
        ),
        migrations.CreateModel(
            name='StickerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Название')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядковый номер')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Описание')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Категория стикеров',
                'verbose_name_plural': 'Категории стикеров',
            },
        ),
        migrations.CreateModel(
            name='Stickers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Название')),
                ('image', models.ImageField(upload_to='stickers/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='common.stickercategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Стикер',
                'verbose_name_plural': 'Стикеры',
            },
        ),
        migrations.CreateModel(
            name='UserPopulateStickers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1, verbose_name='Количество использований пользователем')),
                ('sticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sticker', to='common.stickers', verbose_name='Стикер')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Популярность стикеров',
                'verbose_name_plural': 'Популярность стикеров',
                'ordering': ['-count'],
            },
        ),
        migrations.CreateModel(
            name='UserPopulateSmiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1, verbose_name='Количество использований пользователем')),
                ('smile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='smile', to='common.smiles', verbose_name='Смайл')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Популярность смайликов',
                'verbose_name_plural': 'Популярность смайликов',
                'ordering': ['-count'],
            },
        ),
    ]
