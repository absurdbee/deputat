# Generated by Django 3.2.5 on 2021-09-08 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elect', '0018_elect_is_new'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='elect',
            options={'ordering': ['name'], 'verbose_name': 'Чиновник', 'verbose_name_plural': 'Чиновники'},
        ),
    ]
