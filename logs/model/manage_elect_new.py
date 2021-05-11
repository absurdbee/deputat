from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class ElectNewManageLog(models.Model):
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

    new = models.PositiveIntegerField(default=0, verbose_name="Активность депутатов")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера записи"
        verbose_name_plural = "Логи менеджеров записей"
        ordering=["-created"]


class ElectNewCommentManageLog(models.Model):
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

    comment = models.PositiveIntegerField(default=0, verbose_name="Комментарий к активности депутатов")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера комментария к активности депутатов"
        verbose_name_plural = "Логи менеджеров комментариев к активности депутатов"
        ordering=["-created"]


class ElectNewWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ активностей депутатов'),
        (DELETE_ADMIN, 'Удален админ активностей депутатов'),
        (CREATE_EDITOR, 'Добавлен редактор активностей депутатов'),
        (DELETE_EDITOR, 'Удален редактор активностей депутатов'),
        (CREATE_MODERATOR, 'Добавлен модератор активностей депутатов'),
        (DELETE_MODERATOR, 'Удален модератор активностей депутатов'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера активностей депутатов"
        verbose_name_plural = "Логи суперменеджеров активностей депутатов"
        ordering=["-created"]


class ElectNewCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов активностей депутатов'),
        (DELETE_ADMIN, 'Удален создатель админов активностей депутатов'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов активностей депутатов'),
        (DELETE_EDITOR, 'Удален создатель редакторов запактивностей депутатовисей'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов активностей депутатов'),
        (DELETE_MODERATOR, 'Удален создатель модераторов активностей депутатов'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера активностей депутатов"
        verbose_name_plural = "Логи создателей суперменеджеров активностей депутатов"
        ordering=["-created"]
