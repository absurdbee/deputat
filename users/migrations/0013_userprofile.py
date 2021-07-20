# Generated by Django 3.2 on 2021-05-23 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210514_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(choices=[('NOV', 'Не выбрано'), ('EDH', 'Высшее образование'), ('EDM', 'Среднее специальное'), ('EDL', 'Среднее')], default='NOV', max_length=5, verbose_name='Образование')),
                ('employment', models.CharField(choices=[('NOV', 'Не выбрано'), ('EDU', 'Образование'), ('MED', 'Медицина'), ('IT', 'IT')], default='NOV', max_length=5, verbose_name='Сфера занятости')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('elect_news', models.PositiveIntegerField(default=0, verbose_name='Кол-во постов')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Кол-во просмотров постов')),
                ('friends', models.PositiveIntegerField(default=0, verbose_name='Кол-во друзей')),
                ('follows', models.PositiveIntegerField(default=0, verbose_name='Кол-во подписчиков')),
                ('communities', models.PositiveIntegerField(default=0, verbose_name='Кол-во групп')),
                ('photos', models.PositiveIntegerField(default=0, verbose_name='Кол-во фотографий')),
                ('surveys', models.PositiveIntegerField(default=0, verbose_name='Кол-во опросов')),
                ('docs', models.PositiveIntegerField(default=0, verbose_name='Кол-во документов')),
                ('tracks', models.PositiveIntegerField(default=0, verbose_name='Кол-во аудиозаписей')),
                ('videos', models.PositiveIntegerField(default=0, verbose_name='Кол-во видеозаписей')),
                ('comments', models.PositiveIntegerField(default=0, verbose_name='Кол-во комментов')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Информация о пользователе',
                'verbose_name_plural': 'Информация о пользователях',
            },
        ),
    ]
