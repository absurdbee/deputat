# Generated by Django 3.2 on 2021-04-22 13:55

from django.db import migrations, models
import music.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_music_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='file',
            field=models.FileField(upload_to=music.helpers.upload_to_music_directory, validators=[music.helpers.validate_file_extension], verbose_name='Аудиозапись'),
        ),
    ]
