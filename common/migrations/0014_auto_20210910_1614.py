# Generated by Django 3.2.5 on 2021-09-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_auto_20210907_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electrating',
            name='free_vacation',
            field=models.SmallIntegerField(choices=[(-3, '#FA9D75'), (-2, '#FCB77A'), (-1, '#FDD17F'), (0, '#FFEB84'), (1, '#E0E383'), (2, '#C1DA81'), (3, '#A2D07F')], default=0, verbose_name='Свобода образования'),
        ),
        migrations.AlterField(
            model_name='electrating',
            name='pp_825',
            field=models.SmallIntegerField(choices=[(-3, '#FA9D75'), (-2, '#FCB77A'), (-1, '#FDD17F'), (0, '#FFEB84'), (1, '#E0E383'), (2, '#C1DA81'), (3, '#A2D07F')], default=0, verbose_name='Отмена пп 825'),
        ),
        migrations.AlterField(
            model_name='electrating',
            name='pro_life',
            field=models.SmallIntegerField(choices=[(-3, '#FA9D75'), (-2, '#FCB77A'), (-1, '#FDD17F'), (0, '#FFEB84'), (1, '#E0E383'), (2, '#C1DA81'), (3, '#A2D07F')], default=0, verbose_name='Защита жизни с момента зачатия'),
        ),
        migrations.AlterField(
            model_name='electrating',
            name='safe_family',
            field=models.SmallIntegerField(choices=[(-3, '#FA9D75'), (-2, '#FCB77A'), (-1, '#FDD17F'), (0, '#FFEB84'), (1, '#E0E383'), (2, '#C1DA81'), (3, '#A2D07F')], default=0, verbose_name='Защита прав семьи'),
        ),
        migrations.AlterField(
            model_name='electrating',
            name='vakcine',
            field=models.SmallIntegerField(choices=[(-3, '#FA9D75'), (-2, '#FCB77A'), (-1, '#FDD17F'), (0, '#FFEB84'), (1, '#E0E383'), (2, '#C1DA81'), (3, '#A2D07F')], default=0, verbose_name='Добровольность вакцинации'),
        ),
    ]
