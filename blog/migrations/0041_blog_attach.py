# Generated by Django 3.2.5 on 2022-01-14 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0040_auto_20220112_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='attach',
            field=models.CharField(blank=True, max_length=200, verbose_name='Прикрепленные элементы'),
        ),
    ]
