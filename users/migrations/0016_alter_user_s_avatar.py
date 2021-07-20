# Generated by Django 3.2 on 2021-06-22 17:51

from django.db import migrations
import imagekit.models.fields
import users.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='s_avatar',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to=users.helpers.upload_to_user_directory),
        ),
    ]
