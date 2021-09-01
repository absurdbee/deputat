# Generated by Django 3.2.5 on 2021-08-12 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0005_alter_community_perm'),
        ('blog', '0034_blog_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='electnew',
            name='image',
        ),
        migrations.AddField(
            model_name='electnew',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='elect_new_community', to='communities.community', verbose_name='Сообщество'),
        ),
    ]