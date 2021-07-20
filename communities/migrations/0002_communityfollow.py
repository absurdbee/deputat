# Generated by Django 3.2 on 2021-05-14 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityFollow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.BooleanField(default=False, verbose_name='Просмотрено')),
                ('community', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='community', to='communities.community', verbose_name='На какое сообщество подписывается')),
                ('user', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='community_follows', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписчик группы',
                'verbose_name_plural': 'Подписчики группы',
                'unique_together': {('user', 'community')},
            },
        ),
    ]
