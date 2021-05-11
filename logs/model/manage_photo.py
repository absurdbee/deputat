from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class PhotoManageLog(models.Model):
    LIST_CLOSED, ITEM_CLOSED, COMMENT_CLOSED = 'LCLO', 'ICLO','CCLO'
    LIST_CLOSED_HIDE, ITEM_CLOSED_HIDE, COMMENT_CLOSED_HIDE = 'LRES', 'IRES','CRES'
    LIST_REJECT, ITEM_REJECT, COMMENT_REJECT = 'LREJ', 'IREJ','CREJ'
    LIST_UNVERIFY, ITEM_UNVERIFY, COMMENT_UNVERIFY = 'LUNV', 'IUNV','CUNV'
    ACTION_TYPES = (
        (LIST_CLOSED, 'Список закрыт'),(ITEM_CLOSED, 'Элемент закрыт'),(COMMENT_CLOSED, 'Комментарий закрыт'),
        (LIST_RESTORE, 'Список восстановлен'),(ITEM_RESTORE, 'Элемент восстановлен'),(COMMENT_RESTORE, 'Комментарий восстановлен'),
        (LIST_REJECT, 'Жалоба на список отклонена'),(ITEM_REJECT, 'Жалоба на элемент отклонена'),(COMMENT_REJECT, 'Жалоба на комментарий отклонена'),
        (LIST_UNVERIFY, 'Проверка на список убрана'),(ITEM_UNVERIFY, 'Проверка на элемент убрана'),(COMMENT_UNVERIFY, 'Проверка на комментарий убрана'),
    )

    item = models.PositiveIntegerField(default=0, verbose_name="Список, элемент или коммент")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера фотографий"
        verbose_name_plural = "Логи менеджеров фотографий"
        ordering=["-created"]


class PhotoWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ фотографий'),
        (DELETE_ADMIN, 'Удален админ фотографий'),
        (CREATE_EDITOR, 'Добавлен редактор фотографий'),
        (DELETE_EDITOR, 'Удален редактор фотографий'),
        (CREATE_MODERATOR, 'Добавлен модератор фотографий'),
        (DELETE_MODERATOR, 'Удален модератор фотографий'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера фотографий"
        verbose_name_plural = "Логи суперменеджеров фотографий"
        ordering=["-created"]

class PhotoCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов фотографий'),
        (DELETE_ADMIN, 'Удален создатель админов фотографий'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов фотографий'),
        (DELETE_EDITOR, 'Удален создатель редакторов фотографий'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов фотографий'),
        (DELETE_MODERATOR, 'Удален создатель модераторов фотографий'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера фотографий"
        verbose_name_plural = "Логи создателей суперменеджеров фотографий"
        ordering=["-created"]
