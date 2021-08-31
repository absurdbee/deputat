# Generated by Django 3.2.5 on 2021-08-09 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='point',
            field=models.PositiveIntegerField(default=0, verbose_name='Общее количество кармы'),
        ),
        migrations.AddField(
            model_name='city',
            name='total_costs',
            field=models.PositiveIntegerField(default=0, verbose_name='Общие доходы граждан'),
        ),
        migrations.AddField(
            model_name='city',
            name='total_revenue',
            field=models.PositiveIntegerField(default=0, verbose_name='Общие расходы граждан'),
        ),
    ]
