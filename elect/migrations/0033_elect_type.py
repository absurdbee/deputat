# Generated by Django 3.2.5 on 2021-11-21 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elect', '0032_auto_20211121_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='elect',
            name='type',
            field=models.CharField(choices=[('SUG', 'на рассмотрении'), ('PUB', 'опубликован'), ('DES', 'удален предложенный'), ('DEP', 'удален опубликованый')], default='PUB', max_length=5, verbose_name='Статус депутата'),
        ),
    ]
