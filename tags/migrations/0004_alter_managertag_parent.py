# Generated by Django 3.2 on 2021-07-03 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_alter_managertag_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managertag',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='tags.managertag', verbose_name='Родитель'),
        ),
    ]