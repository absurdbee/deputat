# Generated by Django 3.2.5 on 2021-08-06 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0002_communityfollow'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='city',
            field=models.ManyToManyField(related_name='_communities_community_city_+', to='city.City', verbose_name='Город'),
        ),
    ]
