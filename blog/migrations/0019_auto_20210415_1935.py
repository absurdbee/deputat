# Generated by Django 3.2 on 2021-04-15 19:35

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('elect', '0008_alter_elect_region'),
        ('lists', '0003_delete_region'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0018_auto_20210320_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='electphoto',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='electphoto',
            name='new',
        ),
        migrations.RemoveField(
            model_name='electnew',
            name='tags',
        ),
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='title'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='electnew',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='elect_cat', to='lists.electnewscategory', verbose_name='Категория активности'),
        ),
        migrations.AlterField(
            model_name='electnew',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='elect_new_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
        migrations.RemoveField(
            model_name='electnew',
            name='elect',
        ),
        migrations.AddField(
            model_name='electnew',
            name='elect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_elect', to='elect.elect', verbose_name='Чиновник'),
        ),
        migrations.AlterField(
            model_name='electnew',
            name='status',
            field=models.CharField(choices=[('D', 'Черновик'), ('PG', 'Обработка'), ('P', 'Опубликовано'), ('DE', 'Удалено')], default='P', max_length=2, verbose_name='Статус записи'),
        ),
        migrations.DeleteModel(
            name='ElectDoc',
        ),
        migrations.DeleteModel(
            name='ElectPhoto',
        ),
    ]
