# Generated by Django 3.2 on 2021-04-15 19:42

from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import docs.helpers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('MAI', 'Основной'), ('LIS', 'Пользовательский'), ('DEL', 'Удалённый'), ('PRI', 'Приватный'), ('CLO', 'Закрытый менеджером'), ('MAN', 'Созданный персоналом'), ('PRO', 'Обработка')], default='PRO', max_length=3, verbose_name='Тип листа')),
                ('order', models.PositiveIntegerField(default=1)),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='uuid')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Описание')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_doclist', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('users', models.ManyToManyField(blank=True, related_name='users_doclist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'список документов',
                'verbose_name_plural': 'списки документов',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('file', models.FileField(upload_to=docs.helpers.upload_to_doc_directory, verbose_name='Документ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('status', models.CharField(choices=[('PRO', 'Обработка'), ('PUB', 'Опубликовано'), ('DEL', 'Удалено'), ('PRI', 'Приватно'), ('CLO', 'Закрыто модератором'), ('MAN', 'Созданный персоналом')], default='PRO', max_length=3)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('list', models.ManyToManyField(blank=True, related_name='doc_list', to='docs.DocList')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='doc',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created'], name='docs_doc_created_1fe2f0_brin'),
        ),
    ]
