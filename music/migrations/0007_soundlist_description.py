# Generated by Django 3.2 on 2021-05-17 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_auto_20210513_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='soundlist',
            name='description',
            field=models.CharField(blank=True, max_length=200, verbose_name='Описание'),
        ),
    ]
