from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class OrganizationManageLog(models.Model):
    ITEM_CLOSED, COMMENT_CLOSED = ICLO','CCLO'
    ITEM_CLOSED_HIDE, COMMENT_CLOSED_HIDE = 'IRES','CRES'
    ITEM_REJECT, COMMENT_REJECT = 'IREJ','CREJ'
    ITEM_UNVERIFY, COMMENT_UNVERIFY = 'IUNV','CUNV'
    ACTION_TYPES = (
        (ITEM_CLOSED, 'Элемент закрыт'),(COMMENT_CLOSED, 'Комментарий закрыт'),
        (ITEM_CLOSED_HIDE, 'Элемент восстановлен'),(COMMENT_CLOSED_HIDE, 'Комментарий восстановлен'),
        (ITEM_REJECT, 'Жалоба на элемент отклонена'),(COMMENT_REJECT, 'Жалоба на комментарий отклонена'),
        (ITEM_UNVERIFY, 'Проверка на элемент убрана'),(COMMENT_UNVERIFY, 'Проверка на комментарий убрана'),
    )

    item = models.PositiveIntegerField(default=0, verbose_name="Запись")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера организаций"
        verbose_name_plural = "Логи менеджеров организаций"
        ordering=["-created"]


class OrganizationWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ организаций'),
        (DELETE_ADMIN, 'Удален админ организаций'),
        (CREATE_EDITOR, 'Добавлен редактор организаций'),
        (DELETE_EDITOR, 'Удален редактор организаций'),
        (CREATE_MODERATOR, 'Добавлен модератор организаций'),
        (DELETE_MODERATOR, 'Удален модератор организаций'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера организаций"
        verbose_name_plural = "Логи супеменеджеров организаций"
        ordering=["-created"]

class OrganizationCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов организаций'),
        (DELETE_ADMIN, 'Удален создатель админов организаций'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов организаций'),
        (DELETE_EDITOR, 'Удален создатель редакторов организаций'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов организаций'),
        (DELETE_MODERATOR, 'Удален создатель модераторов организаций'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера организаций"
        verbose_name_plural = "Логи создателей суперменеджеров организаций"
        ordering=["-created"]
