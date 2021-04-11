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
    PROCESSING = 'PRO'
    TYPE = (
        (MAIN, 'Основной'),
        (LIST, 'Пользовательский'),
        (DELETED, 'Удалённый'),
        (PRIVATE, 'Приватный'),
        (CLOSED, 'Закрытый менеджером'),
        (MANAGER, 'Созданный персоналом'),
        (PROCESSING, 'Обработка'),
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
            #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, attach="ldo"+str(list.pk), verb="ITE")
                #send_notify_socket(attach[3:], user_id, "create_doc_list_notify")
            #Wall.objects.create(creator_id=creator.pk, attach="ldo"+str(list.pk), verb="ITE")
            #send_notify_socket(attach[3:], user_id, "create_doc_list_wall")
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
        query = Q(status="PUB") | Q(status="PRI")
        return self.doc_list.filter(query)

    def get_docs(self):
        return self.doc_list.filter(status="PUB")

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
        query = Q(status="PUB") | Q(status="PRI")
        return self.doc_list.filter(query).values("pk").count()

    def is_main_list(self):
        return self.type == self.MAIN
    def is_user_list(self):
        return self.type == self.LIST

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = DocList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(attach="ldo"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="ldo"+str(self.pk), verb="ITE").update(status="C")
        if Wall.objects.filter(attach="ldo"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="ldo"+str(self.pk), verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = DocList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(attach="ldo"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="ldo"+str(self.pk), verb="ITE").update(status="R")
        if Wall.objects.filter(attach="ldo"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="ldo"+str(self.pk), verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        self.type = DocList.DELETED
        self.save(update_fields=['type'])
        if Notify.objects.filter(attach="ldo"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="ldo"+str(self.pk), verb="ITE").update(status="C")
        if Wall.objects.filter(attach="ldo"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="ldo"+str(self.pk), verb="ITE").update(status="C")
    def abort_delete_list(self):
        from notify.models import Notify, Wall
        self.type = DocList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(attach="ldo"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="ldo"+str(self.pk), verb="ITE").update(status="R")
        if Wall.objects.filter(attach="ldo"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="ldo"+str(self.pk), verb="ITE").update(status="R")


class Doc(models.Model):
    PROCESSING = 'PRO'
    PUBLISHED = 'PUB'
    DELETED = 'DEL'
    PRIVATE = 'PRI'
    CLOSED = 'CLO'
    MANAGER = 'MAN'
    STATUS = (
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
    status = models.CharField(choices=STATUS, default=PUBLISHED, max_length=3)
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

    @classmethod
    def create_doc(cls, creator, title, file, lists, is_public):
        #from notify.models import Notify, Wall, get_user_managers_ids
        #from common.notify import send_notify_socket
        from common.processing import get_doc_processing

        doc = cls.objects.create(creator=creator,title=title,file=file)
        if is_public:
            get_doc_processing(doc, Doc.PUBLISHED)
            #for user_id in creator.get_user_news_notify_ids():
            #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, attach="doc"+str(doc.pk), verb="ITE")
                #send_notify_socket(attach[3:], user_id, "create_doc_notify")
            #Wall.objects.create(creator_id=creator.pk, attach="doc"+str(doc.pk), verb="ITE")
            #send_notify_socket(attach[3:], user_id, "create_doc_wall")
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
        self.type = Doc.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(attach="doc"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="doc"+str(self.pk), verb="ITE").update(status="C")
        if Wall.objects.filter(attach="doc"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="doc"+str(self.pk), verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Doc.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(attach="doc"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="doc"+str(self.pk), verb="ITE").update(status="R")
        if Wall.objects.filter(attach="doc"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="doc"+str(self.pk), verb="ITE").update(status="R")

    def delete_doc(self):
        from notify.models import Notify, Wall
        self.status = Doc.DELETED
        self.save(update_fields=['status'])
        if Notify.objects.filter(attach="doc"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="doc"+str(self.pk), verb="ITE").update(status="C")
        if Wall.objects.filter(attach="doc"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="doc"+str(self.pk), verb="ITE").update(status="C")
    def abort_delete_doc(self):
        from notify.models import Notify, Wall
        self.status = Doc.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(attach="doc"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="doc"+str(self.pk), verb="ITE").update(status="R")
        if Wall.objects.filter(attach="doc"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="doc"+str(self.pk), verb="ITE").update(status="R")
