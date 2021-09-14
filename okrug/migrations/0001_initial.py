# Generated by Django 3.2.5 on 2021-09-09 15:09

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('region', '0006_auto_20210809_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Okrug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядковый номер')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='okrug_region', to='region.region', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Одномандатный избирательный округ',
                'verbose_name_plural': 'Одномандатные избирательные округа',
                'ordering': ['order', 'name'],
            },
        ),
    ]