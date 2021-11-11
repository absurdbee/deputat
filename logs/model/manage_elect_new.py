from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class ElectNewManageLog(models.Model):
    LIST_CLOSED, ITEM_CREATED, ITEM_CLOSED, ITEM_PUBLISHED, ITEM_EDITED, COMMENT_CLOSED = 'LCLO','ICRE','ICLO','IPUB','IEDI','CCLO'
    LIST_CLOSED_HIDE, ITEM_CLOSED_HIDE, COMMENT_CLOSED_HIDE = 'LRES','IRES','CRES'
    LIST_REJECT, ITEM_REJECT, COMMENT_REJECT = 'LREJ','IREJ','CREJ'
    LIST_UNVERIFY, ITEM_UNVERIFY, COMMENT_UNVERIFY = 'LUNV','IUNV','CUNV'
    ACTION_TYPES = (
        (LIST_CLOSED, 'Список закрыт'),(ITEM_CREATED, 'Активность создана'),(ITEM_PUBLISHED, 'Активность опубликована'),(ITEM_EDITED, 'Элемент изменён'),(ITEM_CLOSED, 'Элемент закрыт'),(COMMENT_CLOSED, 'Комментарий закрыт'),
        (LIST_CLOSED_HIDE, 'Список восстановлен'),(ITEM_CLOSED_HIDE, 'Элемент восстановлен'),(COMMENT_CLOSED_HIDE, 'Комментарий восстановлен'),
        (LIST_REJECT, 'Жалоба на список отклонена'),(ITEM_REJECT, 'Жалоба на элемент отклонена'),(COMMENT_REJECT, 'Жалоба на комментарий отклонена'),
        (LIST_UNVERIFY, 'Проверка на список убрана'),(ITEM_UNVERIFY, 'Проверка на элемент убрана'),(COMMENT_UNVERIFY, 'Проверка на комментарий убрана'),
    )

    item = models.PositiveIntegerField(default=0, verbose_name="Список, элемент или коммент")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера активностей депутатов"
        verbose_name_plural = "Логи менеджеров активностей депутатов"
        ordering=["-created"]

    def get_item_preview(self):
        try:
            if "I" in self.action_type:
                from blog.models import ElectNew
                new = ElectNew.objects.get(pk=self.item)
                return new.title
            else:
                from common.model.commnets import ElectNewComment
                commnet = ElectNewComment.objects.get(pk=self.item)
                return commnet.text[:25]
        except:
            return "Ошибка"




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


class ElectManageLog(models.Model):
    ITEM_CREATED, ITEM_CLOSED, ITEM_EDITED = 'ICRE','ICLO','IEDI'
    ACTION_TYPES = (
        (ITEM_CREATED, 'Депутат создан'),(ITEM_EDITED, 'Элемент изменён'),(ITEM_CLOSED, 'Элемент закрыт')
    )

    item = models.PositiveIntegerField(default=0, verbose_name="Депутат")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера депутатов"
        verbose_name_plural = "Логи менеджеров депутатов"
        ordering=["-created"]
