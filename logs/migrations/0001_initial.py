# Generated by Django 3.2 on 2021-05-26 15:09

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioCreateWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен создатель админов аудиозаписей'), ('DA', 'Удален создатель админов аудиозаписей'), ('CE', 'Добавлен создатель редакторов аудиозаписей'), ('DE', 'Удален создатель редакторов аудиозаписей'), ('CM', 'Добавлен создатель модераторов аудиозаписей'), ('DM', 'Удален создатель модераторов аудиозаписей')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог создателя суперменеджера аудиозаписей',
                'verbose_name_plural': 'Логи создателей суперменеджеров аудиозаписей',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='AudioManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.PositiveIntegerField(default=0, verbose_name='Запись')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('LCLO', 'Список закрыт'), ('ICLO', 'Элемент закрыт'), ('CCLO', 'Комментарий закрыт'), ('LRES', 'Список восстановлен'), ('IRES', 'Элемент восстановлен'), ('CRES', 'Комментарий восстановлен'), ('LREJ', 'Жалоба на список отклонена'), ('IREJ', 'Жалоба на элемент отклонена'), ('CREJ', 'Жалоба на комментарий отклонена'), ('LUNV', 'Проверка на список убрана'), ('IUNV', 'Проверка на элемент убрана'), ('CUNV', 'Проверка на комментарий убрана')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог менеджера аудиозаписей',
                'verbose_name_plural': 'Логи менеджеров аудиозаписей',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='AudioWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен админ аудиозаписей'), ('DA', 'Удален админ аудиозаписей'), ('CE', 'Добавлен редактор аудиозаписей'), ('DE', 'Удален редактор аудиозаписей'), ('CM', 'Добавлен модератор аудиозаписей'), ('DM', 'Удален модератор аудиозаписей')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог суперменеджера аудиозаписей',
                'verbose_name_plural': 'Логи супеменеджеров аудиозаписей',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='CommunityCreateWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Сообщество')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен создатель админов сообществ'), ('DA', 'Удален создатель админов сообществ'), ('CE', 'Добавлен создатель редакторов сообществ'), ('DE', 'Удален создатель редакторов сообществ'), ('CM', 'Добавлен создатель модераторов сообществ'), ('DM', 'Удален создатель модераторов сообществ'), ('CR', 'Добавлен создатель менеджеров рекламодателей сообществ'), ('DR', 'Удален создатель менеджеров рекламодателей сообществ')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог создателя суперменеджера сообществ',
                'verbose_name_plural': 'Логи создателей суперменеджеров сообществ',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='CommunityManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.PositiveIntegerField(default=0, verbose_name='Сообщество')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CLO', 'Закрыт'), ('CLOH', 'Восстановлен'), ('SC', 'Вечная заморозка'), ('SH', 'Долгая заморозка'), ('SM', 'Средняя заморозка'), ('SL', 'Краткая заморозка'), ('USH', 'Разморожен'), ('WB', 'Выставлен предупреждающий баннер'), ('NWBH', 'Убран предупреждающий баннер'), ('REJ', 'Жалоба отклонена'), ('UNV', 'Проверка убрана')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог менеджера сообществ',
                'verbose_name_plural': 'Логи менеджеров сообществ',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='CommunityWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Сообщество')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен админ сообществ'), ('DA', 'Удален админ сообществ'), ('CE', 'Добавлен редактор сообществ'), ('DE', 'Удален редактор сообществ'), ('CM', 'Добавлен модератор сообществ'), ('DM', 'Удален модератор сообществ'), ('CR', 'Добавлен менеджер рекламодателей сообществ'), ('DR', 'Удален менеджер рекламодателей сообществ')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог суперменеджера сообществ',
                'verbose_name_plural': 'Логи суперменеджеров сообществ',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ElectNewCreateWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен создатель админов активностей депутатов'), ('DA', 'Удален создатель админов активностей депутатов'), ('CE', 'Добавлен создатель редакторов активностей депутатов'), ('DE', 'Удален создатель редакторов запактивностей депутатовисей'), ('CM', 'Добавлен создатель модераторов активностей депутатов'), ('DM', 'Удален создатель модераторов активностей депутатов')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог создателя суперменеджера активностей депутатов',
                'verbose_name_plural': 'Логи создателей суперменеджеров активностей депутатов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ElectNewManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.PositiveIntegerField(default=0, verbose_name='Список, элемент или коммент')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('LCLO', 'Список закрыт'), ('ICLO', 'Элемент закрыт'), ('CCLO', 'Комментарий закрыт'), ('LRES', 'Список восстановлен'), ('IRES', 'Элемент восстановлен'), ('CRES', 'Комментарий восстановлен'), ('LREJ', 'Жалоба на список отклонена'), ('IREJ', 'Жалоба на элемент отклонена'), ('CREJ', 'Жалоба на комментарий отклонена'), ('LUNV', 'Проверка на список убрана'), ('IUNV', 'Проверка на элемент убрана'), ('CUNV', 'Проверка на комментарий убрана')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог менеджера активностей депутатов',
                'verbose_name_plural': 'Логи менеджеров активностей депутатов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ElectNewWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен админ активностей депутатов'), ('DA', 'Удален админ активностей депутатов'), ('CE', 'Добавлен редактор активностей депутатов'), ('DE', 'Удален редактор активностей депутатов'), ('CM', 'Добавлен модератор активностей депутатов'), ('DM', 'Удален модератор активностей депутатов')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог суперменеджера активностей депутатов',
                'verbose_name_plural': 'Логи суперменеджеров активностей депутатов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='PhotoCreateWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен создатель админов фотографий'), ('DA', 'Удален создатель админов фотографий'), ('CE', 'Добавлен создатель редакторов фотографий'), ('DE', 'Удален создатель редакторов фотографий'), ('CM', 'Добавлен создатель модераторов фотографий'), ('DM', 'Удален создатель модераторов фотографий')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог создателя суперменеджера фотографий',
                'verbose_name_plural': 'Логи создателей суперменеджеров фотографий',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='PhotoManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.PositiveIntegerField(default=0, verbose_name='Список, элемент или коммент')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('LCLO', 'Список закрыт'), ('ICLO', 'Элемент закрыт'), ('CCLO', 'Комментарий закрыт'), ('LRES', 'Список восстановлен'), ('IRES', 'Элемент восстановлен'), ('CRES', 'Комментарий восстановлен'), ('LREJ', 'Жалоба на список отклонена'), ('IREJ', 'Жалоба на элемент отклонена'), ('CREJ', 'Жалоба на комментарий отклонена'), ('LUNV', 'Проверка на список убрана'), ('IUNV', 'Проверка на элемент убрана'), ('CUNV', 'Проверка на комментарий убрана')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог менеджера фотографий',
                'verbose_name_plural': 'Логи менеджеров фотографий',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='PhotoWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен админ фотографий'), ('DA', 'Удален админ фотографий'), ('CE', 'Добавлен редактор фотографий'), ('DE', 'Удален редактор фотографий'), ('CM', 'Добавлен модератор фотографий'), ('DM', 'Удален модератор фотографий')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог суперменеджера фотографий',
                'verbose_name_plural': 'Логи суперменеджеров фотографий',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='SurveyCreateWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен создатель админов опросов'), ('DA', 'Удален создатель админов опросов'), ('CE', 'Добавлен создатель редакторов опросов'), ('DE', 'Удален создатель редакторов опросов'), ('CM', 'Добавлен создатель модераторов опросов'), ('DM', 'Удален создатель модераторов опросов')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог создателя суперменеджера опросов',
                'verbose_name_plural': 'Логи создателей суперменеджеров опросов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='SurveyManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.PositiveIntegerField(default=0, verbose_name='Опрос')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('LCLO', 'Список закрыт'), ('ICLO', 'Элемент закрыт'), ('CCLO', 'Комментарий закрыт'), ('LRES', 'Список восстановлен'), ('IRES', 'Элемент восстановлен'), ('CRES', 'Комментарий восстановлен'), ('LREJ', 'Жалоба на список отклонена'), ('IREJ', 'Жалоба на элемент отклонена'), ('CREJ', 'Жалоба на комментарий отклонена'), ('LUNV', 'Проверка на список убрана'), ('IUNV', 'Проверка на элемент убрана'), ('CUNV', 'Проверка на комментарий убрана')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог менеджера опросов',
                'verbose_name_plural': 'Логи менеджеров опросов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='SurveyWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен админ опросов'), ('DA', 'Удален админ опросов'), ('CE', 'Добавлен редактор опросов'), ('DE', 'Удален редактор опросов'), ('CM', 'Добавлен модератор опросов'), ('DM', 'Удален модератор опросов')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог суперменеджера опросов',
                'verbose_name_plural': 'Логи суперменеджеров опросов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='UserCreateWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен создатель админов пользователей'), ('DA', 'Удален создатель админов пользователей'), ('CE', 'Добавлен создатель редакторов пользователей'), ('DE', 'Удален создатель редакторов пользователей'), ('CM', 'Добавлен создатель модераторов пользователей'), ('DM', 'Удален создатель модераторов пользователей'), ('CR', 'Добавлен создатель менеджеров рекламодателей пользователей'), ('DR', 'Удален создатель менеджеров рекламодателей пользователей')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог создателя суперменеджера пользоватетей',
                'verbose_name_plural': 'Логи создателей суперменеджеров пользоватетей',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='UserManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CLO', 'Закрыт'), ('CLOH', 'Восстановлен'), ('SC', 'Вечная заморозка'), ('SH', 'Долгая заморозка'), ('SM', 'Средняя заморозка'), ('SL', 'Краткая заморозка'), ('USH', 'Разморожен'), ('WB', 'Выставлен предупреждающий баннер'), ('NWBH', 'Убран предупреждающий баннер'), ('REJ', 'Жалоба отклонена'), ('UNV', 'Проверка убрана')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог менеджера пользоватетей',
                'verbose_name_plural': 'Логи менеджеров пользоватетей',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='UserWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен админ пользователей'), ('DA', 'Удален админ пользователей'), ('CE', 'Добавлен редактор пользователей'), ('DE', 'Удален редактор пользователей'), ('CM', 'Добавлен модератор пользователей'), ('DM', 'Удален модератор пользователей'), ('CR', 'Добавлен менеджер рекламодателей пользователей'), ('DR', 'Удален менеджер рекламодателей пользователей')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог суперменеджера пользоватетей',
                'verbose_name_plural': 'Логи суперменеджеров пользоватетей',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='VideoCommentManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.PositiveIntegerField(default=0, verbose_name='Комментарий к видеоролику')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('D', 'Удален'), ('UD', 'Восстановлен'), ('R', 'Жалоба отклонена'), ('UV', 'Проверка убрана')], editable=False, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='VideoCreateWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен создатель админов видеороликов'), ('DA', 'Удален создатель админов видеороликов'), ('CE', 'Добавлен создатель редакторов видеороликов'), ('DE', 'Удален создатель редакторов видеороликов'), ('CM', 'Добавлен создатель модераторов видеороликов'), ('DM', 'Удален создатель модераторов видеороликов')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог создателя суперменеджера видеороликов',
                'verbose_name_plural': 'Логи создателей суперменеджеров видеороликов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='VideoManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.PositiveIntegerField(default=0, verbose_name='Запись')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('LCLO', 'Список закрыт'), ('ICLO', 'Элемент закрыт'), ('CCLO', 'Комментарий закрыт'), ('LRES', 'Список восстановлен'), ('IRES', 'Элемент восстановлен'), ('CRES', 'Комментарий восстановлен'), ('LREJ', 'Жалоба на список отклонена'), ('IREJ', 'Жалоба на элемент отклонена'), ('CREJ', 'Жалоба на комментарий отклонена'), ('LUNV', 'Проверка на список убрана'), ('IUNV', 'Проверка на элемент убрана'), ('CUNV', 'Проверка на комментарий убрана')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог менеджера видеороликов',
                'verbose_name_plural': 'Логи менеджеров видеороликов',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='VideoWorkerManageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.PositiveIntegerField(default=0, verbose_name='Пользователь')),
                ('manager', models.PositiveIntegerField(default=0, verbose_name='Менеджер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('action_type', models.CharField(choices=[('CA', 'Добавлен админ видеороликов'), ('DA', 'Удален админ видеороликов'), ('CE', 'Добавлен редактор видеороликов'), ('DE', 'Удален редактор видеороликов'), ('CM', 'Добавлен модератор видеороликов'), ('DM', 'Удален модератор видеороликов')], editable=False, max_length=5)),
            ],
            options={
                'verbose_name': 'Лог суперменеджера видеороликов',
                'verbose_name_plural': 'Логи суперменеджеров видеороликов',
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='videoworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_videow_created_1e3689_brin'),
        ),
        migrations.AddIndex(
            model_name='videomanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_videom_created_42dd0b_brin'),
        ),
        migrations.AddIndex(
            model_name='videocreateworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_videoc_created_824c0d_brin'),
        ),
        migrations.AddIndex(
            model_name='userworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_userwo_created_884608_brin'),
        ),
        migrations.AddIndex(
            model_name='usermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_userma_created_b4d1bc_brin'),
        ),
        migrations.AddIndex(
            model_name='usercreateworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_usercr_created_8cde54_brin'),
        ),
        migrations.AddIndex(
            model_name='surveyworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_survey_created_84b66c_brin'),
        ),
        migrations.AddIndex(
            model_name='surveymanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_survey_created_b32d06_brin'),
        ),
        migrations.AddIndex(
            model_name='surveycreateworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_survey_created_84c458_brin'),
        ),
        migrations.AddIndex(
            model_name='photoworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_photow_created_872f85_brin'),
        ),
        migrations.AddIndex(
            model_name='photomanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_photom_created_fd3694_brin'),
        ),
        migrations.AddIndex(
            model_name='photocreateworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_photoc_created_f47f50_brin'),
        ),
        migrations.AddIndex(
            model_name='electnewworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_electn_created_8e4f89_brin'),
        ),
        migrations.AddIndex(
            model_name='electnewmanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_electn_created_bbce86_brin'),
        ),
        migrations.AddIndex(
            model_name='electnewcreateworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_electn_created_e0d7a1_brin'),
        ),
        migrations.AddIndex(
            model_name='communityworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_commun_created_ac05c9_brin'),
        ),
        migrations.AddIndex(
            model_name='communitymanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_commun_created_8461e1_brin'),
        ),
        migrations.AddIndex(
            model_name='communitycreateworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_commun_created_94be02_brin'),
        ),
        migrations.AddIndex(
            model_name='audioworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_audiow_created_741078_brin'),
        ),
        migrations.AddIndex(
            model_name='audiomanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_audiom_created_2ca5ad_brin'),
        ),
        migrations.AddIndex(
            model_name='audiocreateworkermanagelog',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='logs_audioc_created_a53a52_brin'),
        ),
    ]
