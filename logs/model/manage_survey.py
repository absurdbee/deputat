from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class SurveyManageLog(models.Model):
    LIST_CREATED, LIST_EDITED, LIST_CLOSED, ITEM_CREATED, ITEM_EDITED, ITEM_CLOSED, COMMENT_CLOSED = 'LCRE','LEDI','LCLO','ICRE','IEDI','ICLO','CCLO'
    LIST_CLOSED_HIDE, ITEM_CLOSED_HIDE, COMMENT_CLOSED_HIDE = 'LRES', 'IRES','CRES'
    LIST_REJECT, ITEM_REJECT, COMMENT_REJECT = 'LREJ', 'IREJ','CREJ'
    LIST_UNVERIFY, ITEM_UNVERIFY, COMMENT_UNVERIFY = 'LUNV', 'IUNV','CUNV'
    ACTION_TYPES = (
        (LIST_CREATED, 'Список создан'),(LIST_EDITED, 'Список изменен'),(LIST_CLOSED, 'Список закрыт'),(ITEM_CREATED, 'Элемент создан'),(ITEM_EDITED, 'Элемент изменен'),(ITEM_CLOSED, 'Элемент закрыт'),(COMMENT_CLOSED, 'Комментарий закрыт'),
        (LIST_CLOSED_HIDE, 'Список восстановлен'),(ITEM_CLOSED_HIDE, 'Элемент восстановлен'),(COMMENT_CLOSED_HIDE, 'Комментарий восстановлен'),
        (LIST_REJECT, 'Жалобы на список отклонены'),(ITEM_REJECT, 'Жалобы на элемент отклонены'),(COMMENT_REJECT, 'Жалоба на комментарий отклонены'),
        (LIST_UNVERIFY, 'Проверка на список убрана'),(ITEM_UNVERIFY, 'Проверка на элемент убрана'),(COMMENT_UNVERIFY, 'Проверка на комментарий убрана'),
    )

    item = models.PositiveIntegerField(default=0, verbose_name="Опрос")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера опросов"
        verbose_name_plural = "Логи менеджеров опросов"
        ordering=["-created"]

    def get_item_preview(self):
        try:
            from survey.models import Survey
            survey = Survey.objects.get(pk=self.item)
            return '<a href="/survey/survey_detail/' + str(survey.pk) + '" class="underline" target="_blank" style="font-weight: bold;">' +  survey.title + '</a>'
        except:
            return "Ошибка"


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
