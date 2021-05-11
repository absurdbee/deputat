from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class SurveyManageLog(models.Model):
    DELETED = 'D'
    UNDELETED = 'UD'
    REJECT = 'R'
    UNVERIFY = 'UV'
    ACTION_TYPES = (
        (DELETED, 'Удален'),
        (UNDELETED, 'Восстановлен'),
        (REJECT, 'Жалоба отклонена'),
        (UNVERIFY, 'Проверка убрана'),
    )

    survey = models.PositiveIntegerField(default=0, verbose_name="Опрос")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера опросов"
        verbose_name_plural = "Логи менеджеров опросов"
        ordering=["-created"]


class SurveyWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ опросов'),
        (DELETE_ADMIN, 'Удален админ опросов'),
        (CREATE_EDITOR, 'Добавлен редактор опросов'),
        (DELETE_EDITOR, 'Удален редактор опросов'),
        (CREATE_MODERATOR, 'Добавлен модератор опросов'),
        (DELETE_MODERATOR, 'Удален модератор опросов'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера опросов"
        verbose_name_plural = "Логи суперменеджеров опросов"
        ordering=["-created"]


class SurveyCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов опросов'),
        (DELETE_ADMIN, 'Удален создатель админов опросов'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов опросов'),
        (DELETE_EDITOR, 'Удален создатель редакторов опросов'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов опросов'),
        (DELETE_MODERATOR, 'Удален создатель модераторов опросов'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера опросов"
        verbose_name_plural = "Логи создателей суперменеджеров опросов"
        ordering=["-created"]
