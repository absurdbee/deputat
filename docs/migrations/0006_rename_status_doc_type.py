# Generated by Django 3.2 on 2021-05-22 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0005_auto_20210513_1823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doc',
            old_name='status',
            new_name='type',
        ),
    ]
