import uuid
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q
from django.conf import settings
from gallery.helpers import upload_to_photo_directory
from django.utils import timezone
from communities.models import Community
from django.db.models.signals import post_save
from django.dispatch import receiver


class Album(models.Model):
    MAIN, LIST, MANAGER, PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI'

    DELETED, DELETED_PRIVATE, DELETED_MANAGER = '_DEL', '_DELP', '_DELM'

    CLOSED, CLOSED_PRIVATE, CLOSED_MAIN, CLOSED_MANAGER = '_CLO', '_CLOP', '_CLOM', '_CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PROCESSING, 'Обработка'),

        (DELETED, 'Удалённый'),(DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),

        (CLOSED, 'Закрытый менеджером'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    cover_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, related_name='+', blank=True, null=True, verbose_name="Обожка")
    type = models.CharField(max_length=6, choices=TYPE, default=PROCESSING, verbose_name="Тип альбома")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_album_creator', null=False, blank=False, verbose_name="Создатель")
    community = models.ForeignKey('communities.Community', related_name='photo_lists_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'

    def __str__(self):
        return self.title

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            Album.objects.create(community=instance, type=DocList.MAIN, name="Основной список", order=0, creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            Album.objects.create(creator=instance, type=DocList.MAIN, name="Основной список", order=0)

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

    def is_main_album(self):
        return self.type == self.MAIN
    def is_user_album(self):
        return self.type == self.LIST
    def is_private_album(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.LIST or self.type == self.MAIN or self.type == self.MANAGER

    def get_cover_photo(self):
        if self.cover_photo:
            return self.cover_photo.file.url
        elif self.photo_album.filter(status="PUB").exists():
            return self.photo_album.filter(status="PUB").last().file.url
        else:
            return "/static/images/album.jpg"

    def get_first_photo(self):
        return self.photo_album.filter(status="PUB").first()

    def count_photo(self):
        try:
            return self.photo_album.filter(status="PUB").values("pk").count()
        except:
            return 0
    def count_photo_ru(self):
        count = self.count_photo()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " фотография"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " фотографии"
        else:
            return str(count) + " фотографий"

    def get_photos(self):
        return self.photo_album.filter(status="PUB")

    def get_staff_photos(self):
        query = Q(status="PUB") | Q(status="PRI")
        return self.photo_album.filter(query)

    def is_not_empty(self):
        return self.photo_album.filter(album=self, status="PUB").values("pk").exists()

    def is_item_in_list(self, item_id):
        return self.photo_album.filter(pk=item_id).exists()

    @classmethod
    def create_list(cls, creator, name, description, order, community, is_public):
        from notify.models import Notify, Wall
        from common.processing.photo import get_photo_list_processing
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="PHL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_photo_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="PHL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_photo_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="PHL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_photo_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="PHL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_photo_list_notify")
        get_photo_list_processing(list, Album.LIST)
        return list

    def edit_list(self, title, description, order, is_public):
        from common.processing import get_photo_list_processing

        if not order:
            order = 1
        self.title = name
        self.description = description
        self.order = order
        self.save()
        if is_public:
            get_photo_list_processing(self, Album.LIST)
            self.make_publish()
        else:
            get_photo_list_processing(self, Album.PRIVATE)
            self.make_private()
        return self

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = Album.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Album.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = Album.DELETED
        elif self.type == "PRI":
            self.type = Album.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = Album.DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Album.LIST
        elif self.type == "_DELP":
            self.type = Album.PRIVATE
        elif self.type == "_DELM":
            self.type = Album.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")

    def close_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = Album.CLOSED
        elif self.type == "MAI":
            self.type = Album.CLOSED_MAIN
        elif self.type == "PRI":
            self.type = Album.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = Album.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_list(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Album.LIST
        elif self.type == "_CLOM":
            self.type = Album.MAIN
        elif self.type == "_CLOP":
            self.type = Album.PRIVATE
        elif self.type == "_CLOM":
            self.type = Album.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    @classmethod
    def get_my_albums(cls, user_pk):
        # это все альбомы у request пользователя, кроме основного. И все добавленные альбомы.
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query)

    @classmethod
    def is_have_my_albums(cls, user_pk):
        # есть ли альбомы у request пользователя, кроме основного. И все добавленные альбомы.
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()

    @classmethod
    def get_albums(cls, user_pk):
        # это все альбомы пользователя - пользовательские. И все добавленные им альбомы.
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).order_by("order")

    @classmethod
    def is_have_albums(cls, user_pk):
        # есть ли альбомы пользователя - пользовательские. И все добавленные им альбомы.
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()

    @classmethod
    def get_albums_count(cls, user_pk):
        # это все альбомы пользователя - пользовательские. И все добавленные им альбомы.
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).values("pk").count()


class Photo(models.Model):
    PROCESSING, PUBLISHED, PRIVATE, MANAGER, DELETED, CLOSED = '_PRO','PUB','PRI', 'MAN', '_DEL', '_CLO'
    DELETED_PRIVATE, DELETED_MANAGER, CLOSED_PRIVATE, CLOSED_MANAGER = '_DELP', '_DELM', '_CLOP', '_CLOM'
    STATUS = (
        (PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    album = models.ManyToManyField(Album, related_name="photo_album", blank=True)
    file = ProcessedImageField(format='JPEG', options={'quality': 100}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=1024, upscale=False)])
    preview = ProcessedImageField(format='JPEG', options={'quality': 60}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=102, upscale=False)])
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_creator', null=False, blank=False, verbose_name="Создатель")
    status = models.CharField(max_length=5, choices=STATUS, default=PROCESSING, verbose_name="Тип изображения")
    community = models.ForeignKey('communities.Community', related_name='photo_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ["-created"]

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    @classmethod
    def create_photo(cls, creator, image, list):
        from common.processing.photo import get_photo_processing

        photo = cls.objects.create(creator=creator,preview=image,file=image)
        list.photo_album.add(photo)
        if not list.is_private():
            get_photo_processing(photo, Photo.PUBLISHED)
            if list.community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                community_id = community.pk
                Wall.objects.create(creator_id=creator.pk, community_id=community_id, recipient_id=user_id, type=type, object_id=photo.pk, verb="ITE")
                community_send_wall(photo.pk, creator.pk, community_id, None, "create_c_photo_wall")
                for user_id in list.community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community_id, recipient_id=user_id, type=type, object_id=photo.pk, verb="ITE")
                    community_send_notify(photo.pk, creator.pk, user_id, community_id, None, "create_c_photo_notify")
            else:
                from common.notify.progs import user_send_notify, user_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, type=type, object_id=photo.pk, verb="ITE")
                user_send_wall(photo.pk, None, "create_u_photo_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type=type, object_id=photo.pk, verb="ITE")
                    user_send_notify(photo.pk, creator.pk, user_id, None, "create_u_photo_notify")
        else:
            get_photo_processing(photo, Photo.PRIVATE)
        return photo

    def is_album_exists(self):
        return self.photo_album.filter(creator=self.creator).exists()

    def make_private(self):
        from notify.models import Notify, Wall
        self.status = Photo.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Photo.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")

    def delete_photo(self, community):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Photo.DELETED
        elif self.status == "PRI":
            self.status = Photo.DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Photo.DELETED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_photos(1)
        else:
            self.creator.minus_photos(1)
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_photo(self, community):
        from notify.models import Notify, Wall
        if self.status == "_DEL":
            self.status = Photo.PUBLISHED
        elif self.status == "_DELP":
            self.status = Photo.PRIVATE
        elif self.status == "_DELM":
            self.status = Photo.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_photos(1)
        else:
            self.creator.plus_photos(1)
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")

    def close_doc(self, community):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Photo.CLOSED
        elif self.status == "PRI":
            self.status = Photo.CLOSED_PRIVATE
        elif self.status == "MAN":
            self.status = Photo.CLOSED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_photos(1)
        else:
            self.creator.minus_photos(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_doc(self, community):
        from notify.models import Notify, Wall
        if self.status == "_CLO":
            self.status = Photo.PUBLISHED
        elif self.status == "_CLOP":
            self.status = Photo.PRIVATE
        elif self.status == "_CLOM":
            self.status = Photo.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_photos(1)
        else:
            self.creator.plus_photos(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def get_type(self):
        return self.album.all()[0].type

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED
