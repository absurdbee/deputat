# Generated by Django 3.2 on 2021-05-27 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_alter_soundlist_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soundlist',
            name='type',
            field=models.CharField(choices=[('MAI', 'Основной'), ('LIS', 'Пользовательский'), ('PRI', 'Приватный'), ('MAN', 'Созданный персоналом'), ('_PRO', 'Обработка'), ('_DEL', 'Удалённый'), ('_DELP', 'Удалённый приватный'), ('_DELM', 'Удалённый менеджерский'), ('_CLO', 'Закрытый менеджером'), ('_CLOP', 'Закрытый приватный'), ('_CLOM', 'Закрытый основной'), ('_CLOMA', 'Закрытый менеджерский')], default='_PRO', max_length=6, verbose_name='Тип'),
        ),
    ]
