# Generated by Django 3.2.5 on 2021-10-09 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0009_alter_medialist_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medialist',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_medialist', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
    ]
