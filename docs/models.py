from django.db import models
from django.contrib.postgres.indexes import BrinIndex
import uuid
from django.conf import settings
from docs.helpers import upload_to_doc_directory
from django.db.models import Q


class DocList(models.Model):
    MAIN = 'MAI'
    LIST = 'LIS'
    DELETED = 'DEL'
    PRIVATE = 'PRI'
    CLOSED = 'CLO'
    MANAGER = 'MAN'
    TYPE = (
        (MAIN, 'Основной'),
        (LIST, 'Пользовательский'),
        (DELETED, 'Удалённый'),
        (PRIVATE, 'Приватный'),
        (CLOSED, 'Закрытый менеджером'),
        (MANAGER, 'Созданный персоналом'),
    )
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_doclist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=3, choices=TYPE, default=LIST, verbose_name="Тип листа")
    order = models.PositiveIntegerField(default=1)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")

    users = models.ManyToManyField("users.User", blank=True, related_name='users_doclist')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    def is_item_in_list(self, item_id):
        return self.doc_list.filter(pk=item_id).exists()

    def is_not_empty(self):
        return self.doc_list.filter(list=self).values("pk").exists()

    def get_my_docs(self):
        query = Q(type="PUB") | Q(type="PRI")
        return self.doc_list.filter(query)

    def get_docs(self):
        query = Q(type="PUB")
        queryset = self.doc_list.filter(type="PUB")
        return queryset

    def get_users_ids(self):
        users = self.users.exclude(perm="DE").exclude(perm="BL").exclude(perm="PV").values("pk")
        return [i['pk'] for i in users]

    def is_user_can_add_list(self, user_id):
        if self.creator.pk != user_id and user_id not in self.get_users_ids():
            return True
        else:
            return False
    def is_user_can_delete_list(self, user_id):
        if self.creator.pk != user_id and user_id in self.get_users_ids():
            return True
        else:
            return False

    def count_docs(self):
        query = Q(type="PUB") | Q(type="PRI")
        return self.doc_list.filter(query).values("pk").count()

    def is_main_list(self):
        return self.type == self.MAIN
    def is_user_list(self):
        return self.type == self.LIST

    class Meta:
        verbose_name = "список документов"
        verbose_name_plural = "списки документов"
        ordering = ['order']


class Doc(models.Model):
    PROCESSING = 'PRO'
    PUBLISHED = 'PUB'
    DELETED = 'DEL'
    PRIVATE = 'PRI'
    CLOSED = 'CLO'
    MANAGER = 'MAN'
    TYPES = (
        (PROCESSING, 'Обработка'),
        (PUBLISHED, 'Опубликовано'),
        (DELETED, 'Удалено'),
        (PRIVATE, 'Приватно'),
        (CLOSED, 'Закрыто модератором'),
        (MANAGER, 'Созданный персоналом'),
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to=upload_to_doc_directory, verbose_name="Документ")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    list = models.ManyToManyField(DocList, related_name='doc_list', blank=True)
    type = models.CharField(choices=TYPES, default=PUBLISHED, max_length=3)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_creator', null=False, blank=False, verbose_name="Создатель")

    class Meta:
        ordering = ["-created"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        indexes = (BrinIndex(fields=['created']),)

    def get_lists_for_doc(self):
        return self.list.all()

    def get_mime_type(self):
        import magic
        mime = magic.from_file(self.file.path, mime=True)
        return mime
