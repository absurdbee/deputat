# Generated by Django 3.2.5 on 2021-09-04 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('district', '__first__'),
        ('elect', '0015_auto_20210904_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='elect',
            name='area',
            field=models.ManyToManyField(blank=True, related_name='elect_area', to='district.District2', verbose_name='Районы, за которым закреплен депутат'),
        ),
        migrations.AddField(
            model_name='elect',
            name='post_2',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Должность'),
        ),
    ]
