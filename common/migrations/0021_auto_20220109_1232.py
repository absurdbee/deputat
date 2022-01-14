# Generated by Django 3.2.5 on 2022-01-09 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0020_auto_20220108_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='smilecategory',
            name='classic',
            field=models.BooleanField(default=True, verbose_name='Классические'),
        ),
        migrations.AddField(
            model_name='smilecategory',
            name='gif',
            field=models.BooleanField(default=False, verbose_name='Анимированные'),
        ),
    ]