# Generated by Django 3.2.5 on 2021-12-28 14:53

import chat.helpers
from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0018_smilecategory_smiles_stickercategory_stickers_userpopulatesmiles_userpopulatestickers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Название')),
                ('type', models.CharField(choices=[('PUB', 'Публичный'), ('PRI', 'Приватный'), ('MAN', 'Служебный'), ('GRO', 'Групповой'), ('SUP', 'Техподдержка'), ('_DPUB', 'удал Публичный'), ('_DPRI', 'удал Приватный'), ('_DMAN', 'удал Служебный'), ('_DGRO', 'удал Групповой'), ('_DSUP', 'удал Техподдержка'), ('_CPUB', 'закр. Публичный'), ('_CPRI', 'закр. Приватный'), ('_CMAN', 'закр. Служебный'), ('_CGRO', 'закр. Групповой'), ('_CSUP', 'закр. Техподдержка')], max_length=6, verbose_name='Тип чата')),
                ('image', models.ImageField(blank=True, upload_to=chat.helpers.upload_to_chat_directory)),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Описание')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('members', models.PositiveIntegerField(default=0)),
                ('attach', models.TextField(blank=True, null=True)),
                ('can_add_members', models.PositiveSmallIntegerField(choices=[(1, 'Все участники'), (2, 'Создатель'), (3, 'Создатель и админы'), (4, 'Участники кроме'), (5, 'Некоторые участники')], default=1, verbose_name='Кто приглашает участников')),
                ('can_fix_item', models.PositiveSmallIntegerField(choices=[(1, 'Все участники'), (2, 'Создатель'), (3, 'Создатель и админы'), (4, 'Участники кроме'), (5, 'Некоторые участники')], default=3, verbose_name='Кто закрепляет сообщения')),
                ('can_mention', models.PositiveSmallIntegerField(choices=[(1, 'Все участники'), (2, 'Создатель'), (3, 'Создатель и админы'), (4, 'Участники кроме'), (5, 'Некоторые участники')], default=1, verbose_name='Кто упоминает о беседе')),
                ('can_add_admin', models.PositiveSmallIntegerField(choices=[(1, 'Все участники'), (2, 'Создатель'), (3, 'Создатель и админы'), (4, 'Участники кроме'), (5, 'Некоторые участники')], default=3, verbose_name='Кто назначает админов')),
                ('can_add_design', models.PositiveSmallIntegerField(choices=[(1, 'Все участники'), (2, 'Создатель'), (3, 'Создатель и админы'), (4, 'Участники кроме'), (5, 'Некоторые участники')], default=2, verbose_name='Кто меняет дизайн')),
                ('can_see_settings', models.PositiveSmallIntegerField(choices=[(1, 'Все участники'), (2, 'Создатель'), (3, 'Создатель и админы'), (4, 'Участники кроме'), (5, 'Некоторые участники')], default=2, verbose_name='Кто видит настройки')),
                ('can_see_log', models.PositiveSmallIntegerField(choices=[(1, 'Все участники'), (2, 'Создатель'), (3, 'Создатель и админы'), (4, 'Участники кроме'), (5, 'Некоторые участники')], default=2, verbose_name='Кто видит логи')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Беседа',
                'verbose_name_plural': 'Беседы',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(blank=True, max_length=10000)),
                ('unread', models.BooleanField(db_index=True, default=True, verbose_name='Не прочитано')),
                ('type', models.CharField(choices=[('PFIX', 'Закреп опубл'), ('EFIX', 'Закреп измен'), ('MAN', 'Служебное'), ('PUB', 'Опубл'), ('_DEL', 'Удалено'), ('EDI', 'Изменено'), ('_CLO', 'Закрыто модератором'), ('_DRA', 'Черновик'), ('_DELEF', 'Удал измен закреп'), ('_DELPF', 'Удал опубл закреп'), ('_CLOEF', 'Закр измен закреп'), ('_CLOPF', 'Закр опубл закреп'), ('_CLOPF', 'Закр опубл закреп'), ('_DELE', 'Удал измен'), ('_CLOE', 'Закр измен')], default='PUB', max_length=6, verbose_name='Статус сообщения')),
                ('attach', models.CharField(blank=True, max_length=200, verbose_name='Прикрепленные элементы')),
                ('voice', models.FileField(blank=True, upload_to=chat.helpers.upload_to_chat_directory, verbose_name='Голосовое сообщение')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_message', to='chat.chat')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_thread', to='chat.message')),
                ('sticker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='common.stickers')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='MessageVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(blank=True, max_length=1000)),
                ('attach', models.CharField(blank=True, max_length=200, verbose_name='Прикрепленные элементы')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_version', to='chat.message')),
                ('transfer', models.ManyToManyField(blank=True, related_name='_chat_messageversion_transfer_+', to='chat.MessageVersion')),
            ],
            options={
                'verbose_name': 'Копия сообщения перед изменением',
                'verbose_name_plural': 'Копии сообщений перед изменением',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='MessageTransfers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='chat.message', verbose_name='Сообщение, в котором пересылают')),
                ('transfer', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='chat.message', verbose_name='Сообщение, которое пересылают')),
            ],
        ),
        migrations.CreateModel(
            name='MessageOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Это сообщение пользователь удалил')),
                ('is_favourite', models.BooleanField(default=False, verbose_name='Это сообщение пользователь поместил в избранное')),
                ('message', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='message_options', to='chat.message')),
                ('user', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='message_options_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь-инициатор исключения')),
            ],
        ),
        migrations.CreateModel(
            name='ChatUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_administrator', models.BooleanField(default=False, verbose_name='Это администратор')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('no_disturb', models.DateTimeField(blank=True, null=True, verbose_name='Не беспокоить до...')),
                ('type', models.CharField(choices=[('ACT', 'Действующий'), ('EXI', 'Вышедший'), ('DEL', 'Уделенный')], default='ACT', max_length=3, verbose_name='Тип участника')),
                ('chat', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='chat_relation', to='chat.chat', verbose_name='Чат')),
                ('user', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='chat_users', to=settings.AUTH_USER_MODEL, verbose_name='Члены сообщества')),
            ],
            options={
                'verbose_name': 'участник беседы',
                'verbose_name_plural': 'участники бесед',
            },
        ),
        migrations.CreateModel(
            name='ChatPerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_add_in_chat', models.PositiveSmallIntegerField(choices=[(0, 'Не активно'), (1, 'Может иметь действия с элементом'), (2, 'Не может иметь действия с элементом')], default=0, verbose_name='Кто добавляет в беседы')),
                ('can_add_fix', models.PositiveSmallIntegerField(choices=[(0, 'Не активно'), (1, 'Может иметь действия с элементом'), (2, 'Не может иметь действия с элементом')], default=0, verbose_name='Кто закрепляет сообщения')),
                ('can_send_mention', models.PositiveSmallIntegerField(choices=[(0, 'Не активно'), (1, 'Может иметь действия с элементом'), (2, 'Не может иметь действия с элементом')], default=0, verbose_name='Кто отправляет массовые упоминания')),
                ('can_add_admin', models.PositiveSmallIntegerField(choices=[(0, 'Не активно'), (1, 'Может иметь действия с элементом'), (2, 'Не может иметь действия с элементом')], default=0, verbose_name='Кто добавляет админов и работает с ними')),
                ('can_add_design', models.PositiveSmallIntegerField(choices=[(0, 'Не активно'), (1, 'Может иметь действия с элементом'), (2, 'Не может иметь действия с элементом')], default=0, verbose_name='Кто меняет дизайн')),
                ('can_see_settings', models.PositiveSmallIntegerField(choices=[(0, 'Не активно'), (1, 'Может иметь действия с элементом'), (2, 'Не может иметь действия с элементом')], default=0, verbose_name='Кто видит настройки')),
                ('can_see_log', models.PositiveSmallIntegerField(choices=[(0, 'Не активно'), (1, 'Может иметь действия с элементом'), (2, 'Не может иметь действия с элементом')], default=0, verbose_name='Кто видит журнал действий')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_ie_settings', to='chat.chatusers', verbose_name='Друг')),
            ],
            options={
                'verbose_name': 'Исключения/Включения участника беседы',
                'verbose_name_plural': 'Исключения/Включения участников беседы',
            },
        ),
        migrations.AddIndex(
            model_name='messageversion',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='chat_messag_created_a63fe8_brin'),
        ),
        migrations.AddIndex(
            model_name='messagetransfers',
            index=models.Index(fields=['message', 'transfer'], name='chat_messag_message_d08492_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='messagetransfers',
            unique_together={('message', 'transfer')},
        ),
        migrations.AddIndex(
            model_name='messageoptions',
            index=models.Index(fields=['message', 'user'], name='chat_messag_message_d7fb93_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='messageoptions',
            unique_together={('message', 'user')},
        ),
        migrations.AddIndex(
            model_name='message',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='chat_messag_created_aeee25_brin'),
        ),
        migrations.AddIndex(
            model_name='chatusers',
            index=models.Index(fields=['chat', 'user'], name='chat_chatus_chat_id_277a8e_idx'),
        ),
        migrations.AddIndex(
            model_name='chatusers',
            index=models.Index(fields=['chat', 'user', 'is_administrator'], name='chat_chatus_chat_id_10903e_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='chatusers',
            unique_together={('user', 'chat')},
        ),
        migrations.AlterIndexTogether(
            name='chatperm',
            index_together={('id', 'user')},
        ),
        migrations.AddIndex(
            model_name='chat',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='chat_chat_created_6a9d53_brin'),
        ),
    ]