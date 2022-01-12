# Generated by Django 3.2.5 on 2021-10-02 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0007_auto_20210927_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=1)),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='uuid')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Описание')),
                ('type', models.CharField(choices=[('LIS', 'Основной'), ('_DEL', 'Удалённый')], default='LIS', max_length=4, verbose_name='Тип листа')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_medialist', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_medialist', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'медийный список',
                'verbose_name_plural': 'медийные списки',
                'ordering': ['order'],
            },
        ),
    ]
