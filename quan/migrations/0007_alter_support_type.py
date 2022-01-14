# Generated by Django 3.2.5 on 2021-11-14 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quan', '0006_alter_support_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='type',
            field=models.CharField(choices=[('TP', 'Обращение в техподдержку'), ('QU', 'Вопрос / предложение'), ('CO', 'Сотрудничество'), ('PA', 'Помощь проекту'), ('CH', 'Для правообладателей')], default='QU', max_length=2, verbose_name='Тема'),
        ),
    ]