from django.db import models
from django.contrib.postgres.indexes import BrinIndex
import uuid
from django.conf import settings
from docs.helpers import upload_to_doc_directory, validate_file_extension
from django.db.models import Q
from communities.models import Community
from django.db.models.signals import post_save
from django.dispatch import receiver


class DocList(models.Model):
    MAIN, LIST, MANAGER, PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI'
    DELETED, DELETED_PRIVATE, DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    CLOSED, CLOSED_PRIVATE, CLOSED_MAIN, CLOSED_MANAGER = '_CLO', '_CLOP', '_CLOM', '_CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PROCESSING, 'Обработка'),
        (DELETED, 'Удалённый'),(DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_doclist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=PROCESSING, verbose_name="Тип листа")
    order = models.PositiveIntegerField(default=1)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
    community = models.ForeignKey('communities.Community', related_name='doc_lists_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список документов"
        verbose_name_plural = "списки документов"
        ordering = ['order']

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            DocList.objects.create(community=instance, type=DocList.MAIN, name="Основной список", order=0, creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            DocList.objects.create(creator=instance, type=DocList.MAIN, name="Основной список", order=0)

    @classmethod
    def create_list(cls, creator, name, description, order, community, is_public):
        from notify.models import Notify, Wall
        from common.processing import get_doc_list_processing
        if not DocList.is_user_can_added_list(creator.pk):
            pass
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="DOL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_doc_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="DOL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_doc_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="DOL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_doc_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="POL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_doc_list_notify")
        get_doc_list_processing(list, DocList.LIST)
        return list

    @classmethod
    def create_manager_list(cls, creator, name, description, order):
        from common.processing import get_doc_list_processing
        from logs.model.manage_doc import DocManageLog

        if not order:
            order = 1
        list = cls.objects.create(creator=creator,name=name,description=description,order=order)
        get_doc_list_processing(list, DocList.MANAGER)
        DocManageLog.objects.create(item=self.pk, manager=creator.pk, action_type=DocManageLog.LIST_CREATED)
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

    def edit_manager_list(self, name, description, order, manager_id):
        from common.processing import get_doc_list_processing
        from logs.model.manage_doc import DocManageLog

        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        get_doc_list_processing(self, DocList.MANAGER)
        DocManageLog.objects.create(item=self.pk, manager=manager_id, action_type=DocManageLog.LIST_EDITED)
        return self

    def is_item_in_list(self, item_id):
        return self.doc_list.filter(pk=item_id).exists()

    def is_not_empty(self):
        query = Q(list=self)
        query.add(~Q(type__contains="_"), Q.AND)
        return self.doc_list.filter(query).values("pk").exists()

    def get_staff_items(self):
        return self.doc_list.filter(Q(type="PUB")|Q(type="PRI"))

    def get_items(self):
        return self.doc_list.exclude(type__contains="_")

    def get_penalty_items(self):
        return self.doc_list.filter(type__contains="_CLO")

    def get_users_ids(self):
        users = self.users.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in communities]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids() and self.is_open()
    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def count_items(self):
        return self.doc_list.filter(Q(type="PUB")|Q(type="PRI")).values("pk").count()

    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_private(self):
        return self.type == self.PRIVATE
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_open(self):
        return self.is_main() or self.is_list() or self.type == self.MANAGER
    def is_suspended(self):
        return False

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
        if self.type == "_DEL":
            self.type = DocList.LIST
        elif self.type == "_DELP":
            self.type = DocList.PRIVATE
        elif self.type == "_DELM":
            self.type = DocList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = DocList.CLOSED
        elif self.type == "MAI":
            self.type = DocList.CLOSED_MAIN
        elif self.type == "PRI":
            self.type = DocList.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = DocList.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = DocList.LIST
        elif self.type == "_CLOM":
            self.type = DocList.MAIN
        elif self.type == "_CLOP":
            self.type = DocList.PRIVATE
        elif self.type == "_CLOMA":
            self.type = DocList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(type__contains="_"), Q.AND)
        query.add(~Q(Q(type="MAI")&Q(creator_id=user_pk)), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def get_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(Q(type="MAI")|Q(type="LIS")), Q.AND)
        return cls.objects.filter(query).values("pk").count()
    @classmethod
    def get_user_lists_not_empty(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(Q(type__contains="_")&Q(doc_list__isnull=True)), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_user_can_added_list(cls, user_pk):
        from django.conf import settings
        return cls.get_user_lists_count(user_pk) <= settings.USER_MAX_DOC_LISTS

    @classmethod
    def get_community_staff_lists(cls, community_pk):
        query = Q(community_id=community_pk)|Q(communities__id=community_pk)
        query.add(~Q(type__contains="_"), Q.AND)
        query.add(~Q(Q(type="MAI")&Q(community_id=community_id)), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def get_community_lists(cls, community_pk):
        query = Q(community_id=community_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(community_id=community_pk)|Q(communities__id=community_pk)
        query.add(Q(Q(type="MAI")|Q(type="LIS")), Q.AND)
        return cls.objects.filter(query).values("pk").count()


class Doc(models.Model):
    PROCESSING, PUBLISHED, PRIVATE, MANAGER, DELETED, CLOSED = '_PRO','PUB','PRI', 'MAN', '_DEL', '_CLO'
    DELETED_PRIVATE, DELETED_MANAGER, CLOSED_PRIVATE, CLOSED_MANAGER = '_DELP', '_DELM', '_CLOP', '_CLOM'
    TYPE = (
        (PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to=upload_to_doc_directory, validators=[validate_file_extension], verbose_name="Документ")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    list = models.ManyToManyField(DocList, related_name='doc_list', blank=True)
    media_list = models.ForeignKey("lists.MediaList", on_delete=models.CASCADE, related_name='media_list', null=True, blank=True, verbose_name="Медиа-список")
    type = models.CharField(choices=TYPE, default=PROCESSING, max_length=5)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_creator', null=False, blank=False, verbose_name="Создатель")
    community = models.ForeignKey('communities.Community', related_name='doc_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    class Meta:
        ordering = ["-created"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        indexes = (BrinIndex(fields=['created']),)

    def get_lists(self):
        return self.list.all()

    def get_lists(self):
        return self.list.all()

    @classmethod
    def create_doc(cls, creator, title, file, lists, is_public, community):
        from common.processing import get_doc_processing

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового документа")
        private = 0
        doc = cls.objects.create(creator=creator,title=title,file=file,community=community)
        if community:
            community.plus_docs(1)
        else:
            creator.plus_docs(1)
        for list_id in lists:
            doc_list = DocList.objects.get(pk=list_id)
            doc_list.doc_list.add(doc)
            if doc_list.is_private():
                private = 1
        if not private and is_public:
            get_doc_processing(doc, Doc.PUBLISHED)
            if community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
                community_send_wall(doc.pk, creator.pk, community.pk, None, "create_c_doc_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
                    community_send_notify(doc.pk, creator.pk, user_id, community.pk, None, "create_c_doc_notify")
            else:
                from common.notify.progs import user_send_notify, user_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, type="DOC", object_id=doc.pk, verb="ITE")
                user_send_wall(doc.pk, None, "create_u_doc_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
                    user_send_notify(doc.pk, creator.pk, user_id, None, "create_u_doc_notify")
        else:
            get_doc_processing(doc, Doc.PRIVATE)
        return doc

    @classmethod
    def create_manager_doc(cls, creator, title, file, lists):
        from common.processing import get_doc_processing
        from logs.model.manage_doc import DocManageLog

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового документа")

        doc = cls.objects.create(creator=creator,title=title,file=file)
        for list_id in lists:
            doc_list = DocList.objects.get(pk=list_id)
            doc_list.doc_list.add(doc)

        get_doc_processing(doc, Doc.MANAGER)
        from common.notify.progs import user_send_notify, user_send_wall

        #for user_id in creator.get_user_news_notify_ids():
        #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
        #    user_send_notify(doc.pk, creator.pk, user_id, None, "create_manager_doc_notify")
        DocManageLog.objects.create(item=doc.pk, manager=creator.pk, action_type=DocManageLog.ITEM_CREATED)
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

    def edit_manager_doc(self, title, file, lists, manager_id):
        from common.processing import get_doc_processing
        from logs.model.manage_doc import DocManageLog

        self.title = title
        self.file = file
        self.lists = lists
        get_doc_processing(self, Doc.MANAGER)
        DocManageLog.objects.create(item=self.pk, manager=manager_id, action_type=DocManageLog.ITEM_EDITED)
        return self.save()

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = Doc.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Doc.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def delete_doc(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Doc.DELETED
        elif self.type == "PRI":
            self.type = Doc.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = Doc.DELETED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_doc(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Doc.PUBLISHED
        elif self.type == "_DELP":
            self.type = Doc.PRIVATE
        elif self.type == "_DELM":
            self.type = Doc.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_docs(1)
        else:
            self.creator.plus_docs(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Doc.CLOSED
        elif self.type == "PRI":
            self.type = Doc.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = Doc.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Doc.PUBLISHED
        elif self.type == "_CLOP":
            self.type = Doc.PRIVATE
        elif self.type == "_CLOM":
            self.type = Doc.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_docs(1)
        else:
            self.creator.plus_docs(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_suspended(self):
        return False

    def get_mime_type(self):
        import magic

        file = self.file
        initial_pos = file.tell()
        file.seek(0)
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(initial_pos)
        return mime_type
