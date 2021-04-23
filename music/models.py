import uuid
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from music.helpers import upload_to_music_directory, validate_file_extension
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q


class SoundList(models.Model):
    MAIN, LIST, MANAGER, PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', 'PRO', 'PRI'

    DELETED, DELETED_PRIVATE, DELETED_MANAGER = 'DEL', 'DELP', 'DELM'

    CLOSED, CLOSED_PRIVATE, CLOSED_MAIN, CLOSED_MANAGER = 'CLO', 'CLOP', 'CLOM', 'CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PROCESSING, 'Обработка'),

        (DELETED, 'Удалённый'),(DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),

        (CLOSED, 'Закрытый менеджером'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_playlist', db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=5, choices=TYPE, default=PROCESSING, verbose_name="Тип")
    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 100}, upload_to=upload_to_music_directory, processors=[Transpose(), ResizeToFit(width=400, height=400)])

    users = models.ManyToManyField("users.User", blank=True, related_name='user_soundlist')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список треков"
        verbose_name_plural = "списки треков"
        ordering = ['order']

    def is_item_in_list(self, item_id):
        return self.playlist.filter(pk=item_id).exists()

    def is_not_empty(self):
        return self.playlist.filter(list=self).values("pk").exists()

    def get_my_playlist(self):
        query = Q(status="PUB")|Q(status="PRI")
        return self.playlist.filter(query)

    def get_playlist(self):
        query = Q(status="PUB")
        queryset = self.playlist.filter(query)
        return queryset

    def get_users_ids(self):
        users = self.users.exclude(Q(perm="DE")|Q(perm="BL")).values("pk")
        return [i['pk'] for i in users]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids() and self.is_open()
    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def get_remote_image(self, image_url):
        import os
        from django.core.files import File
        from urllib import request

        result = request.urlretrieve(image_url)
        self.image.save(
            os.path.basename(image_url),
            File(open(result[0], 'rb'))
        )
        self.save()

    def count_tracks(self):
        query = Q(status="PUB") | Q(status="MAN")
        return self.playlist.filter(query).values("pk").count()

    def is_main_list(self):
        return self.type == self.MAIN
    def is_user_list(self):
        return self.type == self.LIST
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.LIST or self.type == self.MAIN or self.type == self.MANAGER

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = SoundList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = SoundList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = SoundList.DELETED
        elif self.type == "PRI":
            self.type = SoundList.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = SoundList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "DEL":
            self.type = SoundList.LIST
        elif self.type == "DELP":
            self.type = SoundList.PRIVATE
        elif self.type == "DELM":
            self.type = SoundList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")

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
        # это все альбомы у request пользователя, кроме основного. И все добавленные альбомы.
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(creator_id=user_pk)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def create_list(cls, creator, name, description, order, is_public):
        #from notify.models import Notify, Wall, get_user_managers_ids
        #from common.notify import send_notify_socket
        from common.processing import get_playlist_processing

        if not order:
            order = 1
        list = cls.objects.create(creator=creator,name=name,description=description, order=order)
        if is_public:
            get_playlist_processing(list, SoundList.LIST)
            #for user_id in creator.get_user_news_notify_ids():
            #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="MUL", object_id=list.pk, verb="ITE")
                #send_notify_socket(object_id, user_id, "create_playlist_notify")
            #Wall.objects.create(creator_id=creator.pk, ype="MUL", object_id=list.pk), verb="ITE")
            #send_notify_socket(object_id, user_id, "create_doc_list_wall")
        else:
            get_playlist_processing(list, SoundList.PRIVATE)
        return list

    def edit_list(self, name, description, order, is_public):
        from common.processing import get_playlist_processing

        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        if is_public:
            get_playlist_processing(self, DocList.LIST)
            self.make_publish()
        else:
            get_playlist_processing(self, DocList.PRIVATE)
            self.make_private()
        return self


class Music(models.Model):
    PROCESSING = 'PRO'
    PUBLISHED = 'PUB'
    DELETED = 'DEL'
    PRIVATE = 'PRI'
    CLOSED = 'CLO'
    MANAGER = 'MAN'
    CLOSED_PRIVATE = 'CLOP'
    DELETED_PRIVATE = 'DELP'
    CLOSED_MANAGER = 'CLOM'
    STATUS = (
        (PROCESSING, 'Обработка'),
        (PUBLISHED, 'Опубликовано'),
        (DELETED, 'Удалено'),
        (PRIVATE, 'Приватно'),
        (CLOSED, 'Закрыто модератором'),
        (MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),
        (CLOSED_PRIVATE, 'Закрытый приватный'),
        (CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    artwork_url = ProcessedImageField(format='JPEG', blank=True, options={'quality': 100}, upload_to=upload_to_music_directory, processors=[Transpose(), ResizeToFit(width=100, height=100)])
    file = models.FileField(upload_to=upload_to_music_directory, validators=[validate_file_extension], verbose_name="Аудиозапись")
    created = models.DateTimeField(default=timezone.now)
    duration = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    list = models.ManyToManyField(SoundList, related_name='playlist', blank="True")
    status = models.CharField(max_length=5, choices=STATUS, default=PROCESSING, verbose_name="Тип")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "треки"
        verbose_name_plural = "треки"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ['-created']

    def get_mp3(self):
        url = self.uri + '/stream?client_id=3ddce5652caa1b66331903493735ddd64d'
        url.replace("\\?", "%3f")
        url.replace("=", "%3d")
        return url
    def get_uri(self):
        if self.file:
            return self.file.url
        else:
            return self.uri
    def get_duration(self):
        if self.duration:
            return self.duration
        else:
            return 0

    def get_remote_image(self, image_url):
        import os
        from django.core.files import File
        from urllib import request

        result = request.urlretrieve(image_url)
        self.artwork_url.save(
            os.path.basename(image_url),
            File(open(result[0], 'rb'))
        )
        self.save()

    def make_private(self):
        from notify.models import Notify, Wall
        self.status = Music.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Music.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def delete_photo(self):
        from notify.models import Notify, Wall
        self.status = Music.DELETED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_photo(self):
        from notify.models import Notify, Wall
        self.status = Music.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def is_private(self):
        return self.status == self.PRIVATE

    @classmethod
    def create_track(cls, creator, title, file, lists, is_public):
        #from notify.models import Notify, Wall, get_user_managers_ids
        #from common.notify import send_notify_socket
        from common.processing import get_music_processing

        track = cls.objects.create(creator=creator,title=title,file=file)
        if is_public:
            get_music_processing(track, Music.PUBLISHED)
            #for user_id in creator.get_user_news_notify_ids():
            #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="MUS", object_id=track.pk, verb="ITE")
                #send_notify_socket(attach[3:], user_id, "create_track_notify")
            #Wall.objects.create(creator_id=creator.pk, type="MUS", object_id=track.pk, verb="ITE")
            #send_notify_socket(attach[3:], user_id, "create_track_wall")
        else:
            get_music_processing(track, Music.PRIVATE)
        for list_id in lists:
            playlist = SoundList.objects.get(pk=list_id)
            playlist.playlist.add(track)
        return track

    def edit_track(self, title, file, lists, is_public):
        from common.processing import get_music_processing

        self.title = title
        self.file = file
        self.lists = lists
        if is_public:
            get_music_processing(self, Music.PUBLISHED)
            self.make_publish()
        else:
            get_music_processing(self, Music.PRIVATE)
            self.make_private()
        return self.save()

    def delete_track(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Music.DELETED
        elif self.status == "PRI":
            self.status = Music.DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Music.DELETED_MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_track(self):
        from notify.models import Notify, Wall
        if self.status == "DEL":
            self.status = Music.PUBLISHED
        elif self.status == "DELP":
            self.status = Music.PRIVATE
        elif self.status == "DELM":
            self.status = Music.MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def get_lists(self):
        return self.list.all()

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED
