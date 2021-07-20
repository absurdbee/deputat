# Generated by Django 3.2 on 2021-04-20 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='status',
            field=models.CharField(choices=[('PRO', 'Обработка'), ('PUB', 'Опубликовано'), ('DEL', 'Удалено'), ('PRI', 'Приватно'), ('CLO', 'Закрыто модератором'), ('MAN', 'Созданный персоналом')], default='PRO', max_length=5, verbose_name='Тип изображения'),
        ),
    ]
