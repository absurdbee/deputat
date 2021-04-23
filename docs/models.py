from django.db import models
from django.contrib.postgres.indexes import BrinIndex
import uuid
from django.conf import settings
from docs.helpers import upload_to_doc_directory, validate_file_extension
from django.db.models import Q


class DocList(models.Model):
    MAIN, LIST, MANAGER, PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', 'PRO', 'PRI'

    DELETED, DELETED_PRIVATE, DELETED_MANAGER = 'DEL', 'DELP', 'DELM'

    CLOSED, CLOSED_PRIVATE, CLOSED_MAIN, CLOSED_MANAGER = 'CLO', 'CLOP', 'CLOM', 'CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PROCESSING, 'Обработка'),

        (DELETED, 'Удалённый'),(DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),

        (CLOSED, 'Закрытый менеджером'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_doclist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=3, choices=TYPE, default=PROCESSING, verbose_name="Тип листа")
    order = models.PositiveIntegerField(default=1)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='users_doclist')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список документов"
        verbose_name_plural = "списки документов"
        ordering = ['order']

    @classmethod
    def create_list(cls, creator, name, description, order, is_public):
        #from notify.models import Notify, Wall, get_user_managers_ids
        #from common.notify import send_notify_socket
        from common.processing import get_doc_list_processing

        if not order:
            order = 1
        list = cls.objects.create(creator=creator,name=name,description=description, order=order)
        if is_public:
            get_doc_list_processing(list, DocList.LIST)
            #for user_id in creator.get_user_news_notify_ids():
            #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="DOL", object_id=list.pk, verb="ITE")
                #send_notify_socket(object_id, user_id, "create_doc_list_notify")
            #Wall.objects.create(creator_id=creator.pk, type="DOL", object_id=list.pk, verb="ITE")
            #send_notify_socket(object_id, user_id, "create_doc_list_wall")
        else:
            get_doc_list_processing(list, DocList.PRIVATE)
        return list

    def edit_list(self, name, description, order, is_public):
        from common.processing import get_doc_list_processing

        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        if is_public:
            get_doc_list_processing(self, DocList.LIST)
            self.make_publish()
        else:
            get_doc_list_processing(self, DocList.PRIVATE)
            self.make_private()
        return self

    def is_item_in_list(self, item_id):
        return self.doc_list.filter(pk=item_id).exists()

    def is_not_empty(self):
        return self.doc_list.filter(list=self).values("pk").exists()

    def get_my_docs(self):
        return self.doc_list.filter(Q(status="PUB")|Q(status="PRI"))

    def get_docs(self):
        return self.doc_list.filter(status="PUB")

    def get_users_ids(self):
        users = self.users.exclude(Q(perm="DE")|Q(perm="BL")).values("pk")
        return [i['pk'] for i in users]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids() and self.is_open()
    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def count_docs(self):
        return self.doc_list.filter(Q(status="PUB")|Q(status="PRI")).values("pk").count()

    def is_main_list(self):
        return self.type == self.MAIN
    def is_user_list(self):
        return self.type == self.LIST
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.is_main_list() or self.is_user_list() or self.type == self.MANAGER

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = DocList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = DocList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = DocList.DELETED
        elif self.type == "PRI":
            self.type = DocList.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = DocList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "DEL":
            self.type = DocList.LIST
        elif self.type == "DELP":
            self.type = DocList.PRIVATE
        elif self.type == "DELM":
            self.type = DocList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    @classmethod
    def get_my_lists(cls, user_pk):
        # это все альбомы у request пользователя, кроме основного. И все добавленные альбомы.
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query)

    @classmethod
    def is_have_my_lists(cls, user_pk):
        # есть ли альбомы у request пользователя, кроме основного. И все добавленные альбомы.
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()

    @classmethod
    def get_lists(cls, user_pk):
        # это все альбомы пользователя - пользовательские. И все добавленные им альбомы.
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).order_by("order")

    @classmethod
    def is_have_lists(cls, user_pk):
        # есть ли альбомы пользователя - пользовательские. И все добавленные им альбомы.
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()

    @classmethod
    def get_lists_count(cls, user_pk):
        # это все альбомы пользователя - пользовательские. И все добавленные им альбомы.
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).values("pk").count()


class Doc(models.Model):
    PROCESSING, PUBLISHED, PRIVATE, MANAGER, DELETED, CLOSED = 'PRO','PUB','PRI', 'MAN', 'DEL', 'CLO'
    DELETED_PRIVATE, DELETED_MANAGER, CLOSED_PRIVATE, CLOSED_MANAGER = 'DELP', 'DELM', 'CLOP', 'CLOM'

    CLOSED_PRIVATE = 'CLOP'
    CLOSED_MANAGER = 'CLOM'
    STATUS = (
        (PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to=upload_to_doc_directory, validators=[validate_file_extension], verbose_name="Документ")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    list = models.ManyToManyField(DocList, related_name='doc_list', blank=True)
    status = models.CharField(choices=STATUS, default=PROCESSING, max_length=5)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_creator', null=False, blank=False, verbose_name="Создатель")

    class Meta:
        ordering = ["-created"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        indexes = (BrinIndex(fields=['created']),)

    def get_lists_for_doc(self):
        return self.list.all()

    @classmethod
    def create_doc(cls, creator, title, file, lists, is_public):
        #from notify.models import Notify, Wall, get_user_managers_ids
        #from common.notify import send_notify_socket
        from common.processing import get_doc_processing

        doc = cls.objects.create(creator=creator,title=title,file=file)
        if is_public:
            get_doc_processing(doc, Doc.PUBLISHED)
            #for user_id in creator.get_user_news_notify_ids():
            #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
                #send_notify_socket(object_id, user_id, "create_doc_notify")
            #Wall.objects.create(creator_id=creator.pk, type="DOC", object_id=doc.pk, verb="ITE")
            #send_notify_socket(object_id, user_id, "create_doc_wall")
        else:
            get_doc_processing(doc, Doc.PRIVATE)
        for list_id in lists:
            doc_list = DocList.objects.get(pk=list_id)
            doc_list.doc_list.add(doc)
        return doc

    def edit_doc(self, title, file, lists, is_public):
        from common.processing import get_doc_processing

        self.title = title
        self.file = file
        self.lists = lists
        if is_public:
            get_doc_processing(self, Doc.PUBLISHED)
            self.make_publish()
        else:
            get_doc_processing(self, Doc.PRIVATE)
            self.make_private()
        return self.save()

    def make_private(self):
        from notify.models import Notify, Wall
        self.status = Doc.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Doc.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def delete_doc(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Doc.DELETED
        elif self.status == "PRI":
            self.status = Doc.DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Doc.DELETED_MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_doc(self):
        from notify.models import Notify, Wall
        if self.status == "DEL":
            self.status = Doc.PUBLISHED
        elif self.status == "DELP":
            self.status = Doc.PRIVATE
        elif self.status == "DELM":
            self.status = Doc.MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED

    def get_mime_type(self):
        import magic

        file = self.file
        initial_pos = file.tell()
        file.seek(0)
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(initial_pos)
        return mime_type
