# Generated by Django 3.2.5 on 2021-11-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elect', '0029_elect_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='elect',
            name='i_address',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Интернет-приёмная'),
        ),
    ]
