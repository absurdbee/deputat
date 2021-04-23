import uuid
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from video.helpers import upload_to_video_directory, validate_file_extension
from django.db.models import Q


class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_videos_count(self):
        return self.video_category.filter(is_deleted=True).values("pk").count()

    def is_video_in_category(self, track_id):
        self.video_category.filter(id=track_id).exists()

    class Meta:
        verbose_name = "Категория ролика"
        verbose_name_plural = "Категории ролика"


class VideoAlbum(models.Model):
    MAIN, LIST, MANAGER, PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', 'PRO', 'PRI'

    DELETED, DELETED_PRIVATE, DELETED_MANAGER = 'DEL', 'DELP', 'DELM'

    CLOSED, CLOSED_PRIVATE, CLOSED_MAIN, CLOSED_MANAGER = 'CLO', 'CLOP', 'CLOM', 'CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PROCESSING, 'Обработка'),

        (DELETED, 'Удалённый'),(DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),

        (CLOSED, 'Закрытый менеджером'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    name = models.CharField(max_length=250, verbose_name="Название")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_user_creator', verbose_name="Создатель")
    type = models.CharField(max_length=5, choices=TYPE, default=PROCESSING, verbose_name="Тип альбома")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='users_video_album')

    class Meta:
        verbose_name = 'Видеоальбом'
        verbose_name_plural = 'Видеоальбомы'
        ordering = ['order']

    def __str__(self):
        return self.title

    @classmethod
    def create_list(cls, creator, name, description, order, is_public):
        #from notify.models import Notify, Wall, get_user_managers_ids
        #from common.notify import send_notify_socket
        from common.processing import get_video_list_processing

        if not order:
            order = 1
        list = cls.objects.create(creator=creator,name=name,description=description, order=order)
        if is_public:
            get_video_list_processing(list, VideoAlbum.LIST)
            #for user_id in creator.get_user_news_notify_ids():
            #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="VIL", object_id=list.pk, verb="ITE")
                #send_notify_socket(object_id, user_id, "create_video_list_notify")
            #Wall.objects.create(creator_id=creator.pk, type="VIL", object_id=list.pk, verb="ITE")
            #send_notify_socket(object_id, user_id, "create_video_list_wall")
        else:
            get_video_list_processing(list, VideoAlbum.PRIVATE)
        return list

    def edit_list(self, name, description, order, is_public):
        from common.processing import get_video_list_processing

        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        if is_public:
            get_video_list_processing(self, VideoAlbum.LIST)
            self.make_publish()
        else:
            get_video_list_processing(self, VideoAlbum.PRIVATE)
            self.make_private()
        return self

    def count_video(self):
        return self.video_album.filter(status="PUB").values("pk").count()

    def get_my_videos(self):
        query = Q(status="PUB") | Q(status="PRI")
        return self.video_album.filter(query)

    def get_videos(self):
        query = Q(status="PUB")
        queryset = self.video_album.filter(status="PUB")
        return queryset

    def get_video_count(self):
        query = Q(status="PUB") | Q(status="PRI")
        return self.video_album.filter(query).values("pk").count()

    def is_main_album(self):
        return self.type == self.MAIN
    def is_user_album(self):
        return self.type == self.LIST
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.LIST or self.type == self.MAIN or self.type == self.MANAGER


    def is_not_empty(self):
        return self.video_album.filter(album=self).values("pk").exists()

    def get_users_ids(self):
        users = self.users.exclude(Q(perm="DE")|Q(perm="BL")).values("pk")
        return [i['pk'] for i in users]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids() and self.is_open()

    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def is_item_in_list(self, item_id):
        return self.video_album.filter(pk=item_id).exists()

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = VideoAlbum.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = VideoAlbum.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = VideoAlbum.DELETED
        elif self.type == "PRI":
            self.type = VideoAlbum.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = VideoAlbum.DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "DEL":
            self.type = VideoAlbum.LIST
        elif self.type == "DELP":
            self.type = VideoAlbum.PRIVATE
        elif self.type == "DELM":
            self.type = VideoAlbum.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")

    @classmethod
    def get_my_video_lists(cls, user_pk):
        # это все альбомы у request пользователя, кроме основного. И все добавленные альбомы.
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query)

    @classmethod
    def is_have_my_video_lists(cls, user_pk):
        # есть ли альбомы у request пользователя, кроме основного. И все добавленные альбомы.
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()

    @classmethod
    def get_video_lists(cls, user_pk):
        # это все альбомы пользователя - пользовательские. И все добавленные им альбомы.
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).order_by("order")

    @classmethod
    def is_have_video_lists(cls, user_pk):
        # есть ли альбомы пользователя - пользовательские. И все добавленные им альбомы.
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()

    @classmethod
    def get_video_lists_count(cls, user_pk):
        # это все альбомы пользователя - пользовательские. И все добавленные им альбомы.
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).values("pk").count()


class Video(models.Model):
    PROCESSING, PUBLISHED, PRIVATE, MANAGER, DELETED, CLOSED = 'PRO','PUB','PRI', 'MAN', 'DEL', 'CLO'
    DELETED_PRIVATE, DELETED_MANAGER, CLOSED_PRIVATE, CLOSED_MANAGER = 'DELP', 'DELM', 'CLOP', 'CLOM'
    STATUS = (
        (PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )

    image = ProcessedImageField(format='JPEG',
                                options={'quality': 90},
                                upload_to=upload_to_video_directory,
                                processors=[ResizeToFit(width=500, upscale=False)],
                                verbose_name="Обложка")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    category = models.ForeignKey(VideoCategory, blank=True, null=True, related_name='video_category', on_delete=models.CASCADE, verbose_name="Категория")
    title = models.CharField(max_length=255, verbose_name="Название")
    uri = models.CharField(max_length=255, verbose_name="Ссылка на видео")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    list = models.ManyToManyField(VideoAlbum, related_name="video_album", blank=True, verbose_name="Альбом")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_creator", on_delete=models.CASCADE, verbose_name="Создатель")
    status = models.CharField(choices=STATUS, default=PROCESSING, max_length=5)
    file = models.FileField(upload_to=upload_to_video_directory, validators=[validate_file_extension], verbose_name="Видеозапись")

    class Meta:
        verbose_name = "Видео-ролики"
        verbose_name_plural = "Видео-ролики"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ['-created']

    def __str__(self):
        return self.title

    @classmethod
    def create_video(cls, creator, title, file, lists, is_public):
        #from notify.models import Notify, Wall, get_user_managers_ids
        #from common.notify import send_notify_socket
        from common.processing import get_video_processing

        video = cls.objects.create(creator=creator,title=title,file=file)
        if is_public:
            get_video_processing(video, Video.PUBLISHED)
            #for user_id in creator.get_user_news_notify_ids():
            #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                #send_notify_socket(object_id, user_id, "create_video_notify")
            #Wall.objects.create(creator_id=creator.pk, type="VID", object_id=video.pk, verb="ITE")
            #send_notify_socket(object_id, user_id, "create_video_wall")
        else:
            get_video_processing(video, VIDEO.PRIVATE)
        for list_id in lists:
            video_list = VIDEO.objects.get(pk=list_id)
            video_list.video_list.add(video)
        return video

    def edit_video(self, title, file, lists, is_public):
        from common.processing import get_video_processing

        self.title = title
        self.file = file
        self.lists = lists
        if is_public:
            get_video_processing(self, VIDEO.PUBLISHED)
            self.make_publish()
        else:
            get_video_processing(self, VIDEO.PRIVATE)
            self.make_private()
        return self.save()

    def get_uri(self):
        if self.file:
            return self.file.url
        else:
            return self.uri

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def likes(self):
        return VideoVotes.objects.filter(parent_id=self.pk, vote__gt=0)

    def visits_count_ru(self):
        count = self.all_visits_count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " просмотр"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " просмотра"
        else:
            return str(count) + " просмотров"

    def all_visits_count(self):
        from stst.models import VideoNumbers
        return VideoNumbers.objects.filter(video=self.pk).values('pk').count()

    def get_albums_for_video(self):
        return self.album.all()
    def get_album_uuid(self):
        return self.album.all()[0].uuid

    def make_private(self):
        from notify.models import Notify, Wall
        self.status = Video.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Video.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def delete_video(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Video.DELETED
        elif self.status == "PRI":
            self.status = Video.DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Video.DELETED_MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_video(self):
        from notify.models import Notify, Wall
        if self.status == "DEL":
            self.status = Video.PUBLISHED
        elif self.status == "DELP":
            self.status = Video.PRIVATE
        elif self.status == "DELM":
            self.status = Video.MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED
