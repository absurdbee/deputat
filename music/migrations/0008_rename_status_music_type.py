# Generated by Django 3.2 on 2021-05-22 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_soundlist_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='music',
            old_name='status',
            new_name='type',
        ),
    ]
