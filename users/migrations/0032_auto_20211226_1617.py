# Generated by Django 3.2.5 on 2021-12-26 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_alter_userprivate_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprivate',
            name='can_add_in_chat',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Все пользователи'), (2, 'На кого я подписан'), (3, 'Никто'), (4, 'На кого я подписан, кроме'), (5, 'Некоторые из тех, на кого я подписан')], default=1, verbose_name='Кто приглашает в беседы'),
        ),
        migrations.AddField(
            model_name='userprivate',
            name='can_send_message',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Все пользователи'), (2, 'На кого я подписан'), (3, 'Никто'), (4, 'На кого я подписан, кроме'), (5, 'Некоторые из тех, на кого я подписан')], default=1, verbose_name='Кто пишет сообщения'),
        ),
        migrations.CreateModel(
            name='FollowPerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_send_message', models.PositiveSmallIntegerField(choices=[(0, 'Не активно'), (1, 'Может иметь действия с элементом'), (2, 'Не может иметь действия с элементом')], default=0, verbose_name='Кто пишет сообщения')),
                ('can_add_in_chat', models.PositiveSmallIntegerField(choices=[(0, 'Не активно'), (1, 'Может иметь действия с элементом'), (2, 'Не может иметь действия с элементом')], default=0, verbose_name='Кто добавляет в беседы')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='connect_ie_settings', to='users.follow', verbose_name='Друг')),
            ],
            options={
                'verbose_name': 'Исключения/Включения followers',
                'verbose_name_plural': 'Исключения/Включения followers',
                'index_together': {('id', 'user')},
            },
        ),
    ]
