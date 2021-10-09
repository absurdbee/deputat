from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class MediaManageLog(models.Model):
    LIST_CREATED,
    LIST_EDITED,
    LIST_DELETED,
    LIST_RECOVER,
    ITEM_CREATED,
    ITEM_EDITED,
    ITEM_DELETED,
    ITEM_RECOVER = 'LCRE','LEDI','LDEL','LREC','ICRE','IEDI','IDEL','IREC'

    ACTION_TYPES = (
        (LIST_CREATED, 'Список создан'),
        (LIST_EDITED, 'Список изменен'),
        (LIST_DELETED, 'Список удален'),
        (LIST_RECOVER, 'Список восстановлен'),
        (ITEM_CREATED, 'Элемент создан'),
        (ITEM_EDITED, 'Элемент изменен'),
        (ITEM_DELETED, 'Элемент удален'),
        (ITEM_RECOVER, 'Элемент восстановлен'),
    )

    item = models.PositiveIntegerField(default=0, verbose_name="Запись")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера медиа-объектов"
        verbose_name_plural = "Логи менеджеров медиа-объектов"
        ordering=["-created"]
