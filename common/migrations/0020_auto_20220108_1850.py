# Generated by Django 3.2.5 on 2022-01-08 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0019_auto_20211229_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='smiles',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Порядковый номер'),
        ),
        migrations.AddField(
            model_name='stickers',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Порядковый номер'),
        ),
    ]