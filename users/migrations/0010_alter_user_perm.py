# Generated by Django 3.2 on 2021-05-12 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210415_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='perm',
            field=models.CharField(choices=[('_PV', 'Телефон не подтвержден'), ('STA', 'Обычные права'), ('VES', 'Запрос на проверку'), ('VER', 'Проверенный'), ('IDS', 'Запрос на идентификацию'), ('IDE', 'Идентифицированный'), ('MAN', 'Менеджер'), ('SUP', 'Суперменеджер'), ('_DELS', 'Удален'), ('_DELVS', 'Удален подавший на верификацию'), ('_DELV', 'Удален верифицированный'), ('_DELIS', 'Удален подавший на идентификацию'), ('_DELI', 'Удален идентифиированный'), ('_DELM', 'Удален менеджер'), ('_CLOS', 'Закрыт'), ('_CLOVS', 'Удален подавший на верификацию'), ('_CLOV', 'Закрыт верифицированный'), ('_CLOIS', 'Закрыт подавший на идентификацию'), ('_CLOI', 'Закрыт идентифиированный'), ('_CLOM', 'Закрыт менеджер'), ('_SUSS', 'Заморожен'), ('_SUSVS', 'Заморожен подавший на верификацию'), ('_SUSV', 'Заморожен верифицированный'), ('_SUSIS', 'Заморожен подавший на идентификацию'), ('_SUSI', 'Заморожен идентифиированный'), ('_SUSM', 'Заморожен менеджер'), ('_BANS', 'Баннер'), ('_BANVS', 'Баннер подавший на верификацию'), ('_BANV', 'Баннер верифицированный'), ('_BANIS', 'Баннер подавший на идентификацию'), ('_BANI', 'Баннер идентифиированный'), ('_BANM', 'Баннер менеджер')], default='_PV', max_length=6, verbose_name='Уровень доступа'),
        ),
    ]
