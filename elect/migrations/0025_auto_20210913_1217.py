# Generated by Django 3.2.5 on 2021-09-13 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elect', '0024_auto_20210913_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elect',
            name='address',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Адрес (приёмная)'),
        ),
        migrations.AlterField(
            model_name='elect',
            name='fb',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Ссылка на Facebook'),
        ),
        migrations.AlterField(
            model_name='elect',
            name='ig',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Ссылка на Instagram'),
        ),
        migrations.AlterField(
            model_name='elect',
            name='mail',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='elect',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='elect',
            name='tg',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Ссылка на Telegram'),
        ),
        migrations.AlterField(
            model_name='elect',
            name='tw',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Ссылка на Twitter'),
        ),
        migrations.AlterField(
            model_name='elect',
            name='vk',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Ссылка на VK'),
        ),
    ]
