# Generated by Django 3.2.5 on 2021-09-04 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elect', '0016_auto_20210904_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='elect',
            name='old',
            field=models.BooleanField(default=False, verbose_name='Старый депутат'),
        ),
    ]