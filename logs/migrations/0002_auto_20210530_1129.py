# Generated by Django 3.2 on 2021-05-30 11:29

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocCreateWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен создатель админов документов'), ('DA', 'Удален создатель админов документов'), ('CE', 'Добавлен создатель редакторов документов'), ('DE', 'Удален создатель редакторов документов'), ('CM', 'Добавлен создатель модераторов документов'), ('DM', 'Удален создатель модераторов документов')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог создателя суперменеджера документов',
                'verbose_name_plural': 'Логи создателей суперменеджеров документов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='DocManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.PositiveIntegerField(default=0, verbose_name='Запись')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('LCLO', 'Список закрыт'), ('ICLO', 'Элемент закрыт'), ('CCLO', 'Комментарий закрыт'), ('LRES', 'Список восстановлен'), ('IRES', 'Элемент восстановлен'), ('CRES', 'Комментарий восстановлен'), ('LREJ', 'Жалоба на список отклонена'), ('IREJ', 'Жалоба на элемент отклонена'), ('CREJ', 'Жалоба на комментарий отклонена'), ('LUNV', 'Проверка на список убрана'), ('IUNV', 'Проверка на элемент убрана'), ('CUNV', 'Проверка на комментарий убрана')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог менеджера документов',
                'verbose_name_plural': 'Логи менеджеров документов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='DocWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен админ документов'), ('DA', 'Удален админ документов'), ('CE', 'Добавлен редактор документов'), ('DE', 'Удален редактор документов'), ('CM', 'Добавлен модератор документов'), ('DM', 'Удален модератор документов')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог суперменеджера документов',
                'verbose_name_plural': 'Логи супеменеджеров документов',
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='docworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_docwor_created_f1518d_brin'),
        ),
        migrations.AddIndex(
            model_name='docmanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_docman_created_eab4a7_brin'),
        ),
        migrations.AddIndex(
            model_name='doccreateworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_doccre_created_b8636b_brin'),
        ),
    ]
