# Generated by Django 3.2.5 on 2021-12-26 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0008_auto_20210830_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notify',
            name='verb',
            field=models.CharField(choices=[('ITE', ' разместил'), ('ELNC', 'Ваша новость одобрена'), ('COMC', 'Ваше сообщество одобрено'), ('ORGC', 'Ваша организация одобрено'), ('ELEC', 'Чиновник одобрен'), ('COM', ' написал'), ('WCOM', ' написала'), ('GCOM', ' написали'), ('REP', ' ответил на'), ('WREP', ' ответила на'), ('GREP', ' ответили на'), ('LIK', ' оценил'), ('WLIK', ' оценила'), ('GLIK', ' оценили'), ('DIS', ' не оценил'), ('WDIS', ' не оценила'), ('GDIS', ' не оценили'), ('INE', ' считает, что'), ('WINE', ' считает, что'), ('GINE', ' считает, что'), ('LCO', ' оценил'), ('WLCO', ' оценила '), ('GLCO', ' оценили'), ('LRE', ' оценил'), ('WLRE', ' оценила'), ('GLRE', ' оценили'), ('SVO', ' участвовал в опросе'), ('WSVO', ' участвовала в опросе'), ('GSVO', ' участвовали в опросе'), ('CRE', ' подал заявку в'), ('WCRE', ' подала заявку в'), ('GCRE', ' подали заявку в'), ('CCO', ' принят в'), ('WCCO', ' принята'), ('GCCO', ' приняты'), ('REG', ' зарегистрировался'), ('WREG', ' зарегистрировалась'), ('GREG', ' зарегистрировались')], max_length=5, verbose_name='Тип уведомления'),
        ),
        migrations.AlterField(
            model_name='wall',
            name='verb',
            field=models.CharField(choices=[('ITE', ' разместил'), ('ELNC', 'Ваша новость одобрена'), ('COMC', 'Ваше сообщество одобрено'), ('ORGC', 'Ваша организация одобрено'), ('ELEC', 'Чиновник одобрен'), ('COM', ' написал'), ('WCOM', ' написала'), ('GCOM', ' написали'), ('REP', ' ответил на'), ('WREP', ' ответила на'), ('GREP', ' ответили на'), ('LIK', ' оценил'), ('WLIK', ' оценила'), ('GLIK', ' оценили'), ('DIS', ' не оценил'), ('WDIS', ' не оценила'), ('GDIS', ' не оценили'), ('INE', ' считает, что'), ('WINE', ' считает, что'), ('GINE', ' считает, что'), ('LCO', ' оценил'), ('WLCO', ' оценила '), ('GLCO', ' оценили'), ('LRE', ' оценил'), ('WLRE', ' оценила'), ('GLRE', ' оценили'), ('SVO', ' участвовал в опросе'), ('WSVO', ' участвовала в опросе'), ('GSVO', ' участвовали в опросе'), ('CRE', ' подал заявку в'), ('WCRE', ' подала заявку в'), ('GCRE', ' подали заявку в'), ('CCO', ' принят в'), ('WCCO', ' принята'), ('GCCO', ' приняты'), ('REG', ' зарегистрировался'), ('WREG', ' зарегистрировалась'), ('GREG', ' зарегистрировались')], max_length=5, verbose_name='Тип уведомления'),
        ),
    ]
