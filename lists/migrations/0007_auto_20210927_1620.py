# Generated by Django 3.2.5 on 2021-09-27 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_authoritylist_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorityListCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории блога')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядковый номер')),
            ],
            options={
                'verbose_name': 'Категория органа власти',
                'verbose_name_plural': 'Категории органов власти',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.RemoveField(
            model_name='authoritylist',
            name='year',
        ),
        migrations.AddField(
            model_name='authoritylist',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='lists.authoritylistcategory', verbose_name='Категория органа власти'),
        ),
    ]