# Generated by Django 3.2.5 on 2021-11-10 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elect', '0028_auto_20211024_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='elect',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удаленный депутат'),
        ),
    ]