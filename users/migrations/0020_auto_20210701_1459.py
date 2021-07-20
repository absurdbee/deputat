# Generated by Django 3.2 on 2021-07-01 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20210626_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('_PV', 'Телефон не подтвержден'), ('STA', 'Обычные права'), ('DEP', 'Депутат'), ('DEPS', 'Запрос на депутатство'), ('VES', 'Запрос на проверку'), ('VER', 'Проверенный'), ('IDS', 'Запрос на идентификацию'), ('IDE', 'Идентифицированный'), ('MAN', 'Менеджер'), ('SUP', 'Суперменеджер'), ('_DELD', 'Удален депутат'), ('_DELDS', 'Удален подавший на депутатство'), ('_DELS', 'Удален'), ('_DELVS', 'Удален подавший на верификацию'), ('_DELV', 'Удален верифицированный'), ('_DELIS', 'Удален подавший на идентификацию'), ('_DELI', 'Удален идентифиированный'), ('_DELM', 'Удален менеджер'), ('_CLOD', 'Закрыт депутат'), ('_CLODS', 'Закрыт подавший на депутатство'), ('_CLOS', 'Закрыт'), ('_CLOVS', 'Удален подавший на верификацию'), ('_CLOV', 'Закрыт верифицированный'), ('_CLOIS', 'Закрыт подавший на идентификацию'), ('_CLOI', 'Закрыт идентифиированный'), ('_CLOM', 'Закрыт менеджер'), ('_SUSD', 'Заморожен депутат'), ('_SUSDS', 'Заморожен подавший на депутатство'), ('_SUSS', 'Заморожен'), ('_SUSVS', 'Заморожен подавший на верификацию'), ('_SUSV', 'Заморожен верифицированный'), ('_SUSIS', 'Заморожен подавший на идентификацию'), ('_SUSI', 'Заморожен идентифиированный'), ('_SUSM', 'Заморожен менеджер'), ('_BAND', 'Баннер депутат'), ('_BANDS', 'Баннер подавший на депутатство'), ('_BANS', 'Баннер'), ('_BANVS', 'Баннер подавший на верификацию'), ('_BANV', 'Баннер верифицированный'), ('_BANIS', 'Баннер подавший на идентификацию'), ('_BANI', 'Баннер идентифиированный'), ('_BANM', 'Баннер менеджер')], default='_PV', max_length=6, verbose_name='Уровень доступа'),
        ),
        migrations.CreateModel(
            name='UserSecretKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=20, verbose_name='Ключ доступа')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='DeputatSend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=500, verbose_name='Описание спообов идентификации')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
