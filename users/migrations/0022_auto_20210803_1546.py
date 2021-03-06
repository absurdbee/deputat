# Generated by Django 3.2.5 on 2021-08-03 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20210801_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='total_costs',
            field=models.PositiveIntegerField(default=0, verbose_name='Доходы'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_revenue',
            field=models.PositiveIntegerField(default=0, verbose_name='Расходы'),
        ),
    ]
