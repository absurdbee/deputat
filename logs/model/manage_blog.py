from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class BlogManageLog(models.Model):
    LIST_CLOSED, ITEM_CREATED, ITEM_CLOSED, ITEM_EDITED, COMMENT_CLOSED = 'LCLO','ICRE','ICLO','IEDI','CCLO'
    LIST_CLOSED_HIDE, ITEM_CLOSED_HIDE, COMMENT_CLOSED_HIDE = 'LRES','IRES','CRES'
    LIST_REJECT, ITEM_REJECT, COMMENT_REJECT = 'LREJ','IREJ','CREJ'
    LIST_UNVERIFY, ITEM_UNVERIFY, COMMENT_UNVERIFY = 'LUNV','IUNV','CUNV'
    ACTION_TYPES = (
        (LIST_CLOSED, 'Список закрыт'),(ITEM_CREATED, 'Новость создана'),(ITEM_EDITED, 'Элемент изменён'),(ITEM_CLOSED, 'Элемент закрыт'),(COMMENT_CLOSED, 'Комментарий закрыт'),
        (LIST_CLOSED_HIDE, 'Список восстановлен'),(ITEM_CLOSED_HIDE, 'Элемент восстановлен'),(COMMENT_CLOSED_HIDE, 'Комментарий восстановлен'),
        (LIST_REJECT, 'Жалоба на список отклонена'),(ITEM_REJECT, 'Жалоба на элемент отклонена'),(COMMENT_REJECT, 'Жалоба на комментарий отклонена'),
        (LIST_UNVERIFY, 'Проверка на список убрана'),(ITEM_UNVERIFY, 'Проверка на элемент убрана'),(COMMENT_UNVERIFY, 'Проверка на комментарий убрана'),
    )

    item = models.PositiveIntegerField(default=0, verbose_name="Запись")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера блога"
        verbose_name_plural = "Логи менеджеров блога"
        ordering=["-created"]


class BlogWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ блога'),
        (DELETE_ADMIN, 'Удален админ блога'),
        (CREATE_EDITOR, 'Добавлен редактор блога'),
        (DELETE_EDITOR, 'Удален редактор блога'),
        (CREATE_MODERATOR, 'Добавлен модератор блога'),
        (DELETE_MODERATOR, 'Удален модератор блога'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера блога"
        verbose_name_plural = "Логи супеменеджеров блога"
        ordering=["-created"]

class BlogCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов блога'),
        (DELETE_ADMIN, 'Удален создатель админов блога'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов блога'),
        (DELETE_EDITOR, 'Удален создатель редакторов блога'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов блога'),
        (DELETE_MODERATOR, 'Удален создатель модераторов блога'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера блога"
        verbose_name_plural = "Логи создателей суперменеджеров блога"
        ordering=["-created"]
