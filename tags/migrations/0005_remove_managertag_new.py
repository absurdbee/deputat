# Generated by Django 3.2.5 on 2021-08-30 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0004_alter_managertag_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='managertag',
            name='new',
        ),
    ]
