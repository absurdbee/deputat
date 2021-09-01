# Generated by Django 3.2.5 on 2021-08-09 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0005_alter_region_svg'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='point',
            field=models.PositiveIntegerField(default=0, verbose_name='Общее количество кармы'),
        ),
        migrations.AddField(
            model_name='region',
            name='total_costs',
            field=models.PositiveIntegerField(default=0, verbose_name='Общие доходы граждан'),
        ),
        migrations.AddField(
            model_name='region',
            name='total_revenue',
            field=models.PositiveIntegerField(default=0, verbose_name='Общие расходы граждан'),
        ),
    ]