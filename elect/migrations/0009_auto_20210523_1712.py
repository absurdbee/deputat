# Generated by Django 3.2 on 2021-05-23 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elect', '0008_alter_elect_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='elect',
            name='dislike',
            field=models.PositiveIntegerField(default=0, verbose_name='Кол-во дизлайков'),
        ),
        migrations.AddField(
            model_name='elect',
            name='inert',
            field=models.PositiveIntegerField(default=0, verbose_name='Кол-во inert'),
        ),
        migrations.AddField(
            model_name='elect',
            name='like',
            field=models.PositiveIntegerField(default=0, verbose_name='Кол-во лайков'),
        ),
        migrations.AddField(
            model_name='elect',
            name='repost',
            field=models.PositiveIntegerField(default=0, verbose_name='Кол-во репостов'),
        ),
        migrations.AddField(
            model_name='elect',
            name='view',
            field=models.PositiveIntegerField(default=0, verbose_name='Кол-во просмотров'),
        ),
    ]
