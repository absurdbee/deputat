# Generated by Django 3.2 on 2021-06-26 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_user_s_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='birthday',
        ),
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='День рождения'),
        ),
    ]
