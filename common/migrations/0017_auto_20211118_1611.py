# Generated by Django 3.2.5 on 2021-11-18 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_alter_blogcomment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electnewcomment',
            name='text',
            field=models.TextField(blank=True, max_length=3000),
        ),
        migrations.AlterField(
            model_name='organizationcomment',
            name='text',
            field=models.TextField(blank=True, max_length=3000),
        ),
    ]