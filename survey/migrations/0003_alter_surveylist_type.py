# Generated by Django 3.2 on 2021-05-27 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_rename_status_survey_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveylist',
            name='type',
            field=models.CharField(choices=[('MAI', 'Основной'), ('LIS', 'Пользовательский'), ('MAN', 'Созданный персоналом'), ('_PRO', 'Обработка'), ('_DEL', 'Удалённый'), ('_DELM', 'Удалённый менеджерский'), ('_CLO', 'Закрытый менеджером'), ('_CLOP', 'Закрытый приватный'), ('_CMAI', 'Закрытый основной'), ('_CLOMA', 'Закрытый менеджерский')], default='_PRO', max_length=6, verbose_name='Тип списка'),
        ),
    ]
