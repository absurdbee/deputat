from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class DocManageLog(models.Model):
    LIST_CREATED, LIST_EDITED, LIST_CLOSED, ITEM_CREATED, ITEM_EDITED, ITEM_CLOSED, COMMENT_CLOSED = 'LCRE','LEDI','LCLO','ICRE','IEDI','ICLO','CCLO'
    LIST_CLOSED_HIDE, ITEM_CLOSED_HIDE, COMMENT_CLOSED_HIDE = 'LRES', 'IRES','CRES'
    LIST_REJECT, ITEM_REJECT, COMMENT_REJECT = 'LREJ', 'IREJ','CREJ'
    LIST_UNVERIFY, ITEM_UNVERIFY, COMMENT_UNVERIFY = 'LUNV', 'IUNV','CUNV'
    ACTION_TYPES = (
        (LIST_CREATED, 'Список создан'),(LIST_EDITED, 'Список изменен'),(LIST_CLOSED, 'Список закрыт'),(ITEM_CREATED, 'Элемент создан'),(ITEM_EDITED, 'Элемент изменен'),(ITEM_CLOSED, 'Элемент закрыт'),(COMMENT_CLOSED, 'Комментарий закрыт'),
        (LIST_CLOSED_HIDE, 'Список восстановлен'),(ITEM_CLOSED_HIDE, 'Элемент восстановлен'),(COMMENT_CLOSED_HIDE, 'Комментарий восстановлен'),
        (LIST_REJECT, 'Жалобы на список отклонены'),(ITEM_REJECT, 'Жалобы на элемент отклонены'),(COMMENT_REJECT, 'Жалобы на комментарий отклонены'),
        (LIST_UNVERIFY, 'Проверка на список убрана'),(ITEM_UNVERIFY, 'Проверка на элемент убрана'),(COMMENT_UNVERIFY, 'Проверка на комментарий убрана'),
    )

    item = models.PositiveIntegerField(default=0, verbose_name="Запись")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера документов"
        verbose_name_plural = "Логи менеджеров документов"
        ordering=["-created"]

    def get_item_preview(self):
        try:
            from docs.models import Doc
            doc = Doc.objects.get(pk=self.item)
            return '<a href="/docs/doc_detail/' + str(doc.pk) + '" class="underline" target="_blank" style="font-weight: bold;">' +  doc.title + '</a>'
        except:
            return "Ошибка"


class DocWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ документов'),
        (DELETE_ADMIN, 'Удален админ документов'),
        (CREATE_EDITOR, 'Добавлен редактор документов'),
        (DELETE_EDITOR, 'Удален редактор документов'),
        (CREATE_MODERATOR, 'Добавлен модератор документов'),
        (DELETE_MODERATOR, 'Удален модератор документов'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера документов"
        verbose_name_plural = "Логи супеменеджеров документов"
        ordering=["-created"]

class DocCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов документов'),
        (DELETE_ADMIN, 'Удален создатель админов документов'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов документов'),
        (DELETE_EDITOR, 'Удален создатель редакторов документов'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов документов'),
        (DELETE_MODERATOR, 'Удален создатель модераторов документов'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера документов"
        verbose_name_plural = "Логи создателей суперменеджеров документов"
        ordering=["-created"]
