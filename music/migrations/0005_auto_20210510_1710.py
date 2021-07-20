# Generated by Django 3.2 on 2021-05-10 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20210423_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='status',
            field=models.CharField(choices=[('_PRO', 'Обработка'), ('PUB', 'Опубликовано'), ('_DEL', 'Удалено'), ('PRI', 'Приватно'), ('_CLO', 'Закрыто модератором'), ('MAN', 'Созданный персоналом'), ('_DELP', 'Удалённый приватный'), ('_DELM', 'Удалённый менеджерский'), ('_CLOP', 'Закрытый приватный'), ('_CLOM', 'Закрытый менеджерский')], default='_PRO', max_length=5, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='soundlist',
            name='type',
            field=models.CharField(choices=[('MAI', 'Основной'), ('LIS', 'Пользовательский'), ('PRI', 'Приватный'), ('MAN', 'Созданный персоналом'), ('_PRO', 'Обработка'), ('_DEL', 'Удалённый'), ('_DELP', 'Удалённый приватный'), ('_DELM', 'Удалённый менеджерский'), ('_CLO', 'Закрытый менеджером'), ('_CLOP', 'Закрытый приватный'), ('_CLOM', 'Закрытый основной'), ('_CLOMA', 'Закрытый менеджерский')], default='_PRO', max_length=6, verbose_name='Тип'),
        ),
    ]
