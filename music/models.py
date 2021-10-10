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
from communities.models import Community
from django.db.models.signals import post_save
from django.dispatch import receiver


class SoundList(models.Model):
    MAIN, LIST, MANAGER, PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI'
    DELETED, DELETED_PRIVATE, DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    CLOSED, CLOSED_PRIVATE, CLOSED_MAIN, CLOSED_MANAGER = '_CLO', '_CLOP', '_CLOM', '_CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PROCESSING, 'Обработка'),
        (DELETED, 'Удалённый'),(DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='playlist_creator', db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=PROCESSING, verbose_name="Тип")
    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 100}, upload_to=upload_to_music_directory, processors=[Transpose(), ResizeToFit(width=400, height=400)])
    community = models.ForeignKey('communities.Community', related_name='playlist_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список треков"
        verbose_name_plural = "списки треков"
        ordering = ['order']

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            SoundList.objects.create(community=instance, type=SoundList.MAIN, name="Основной список", order=0, creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            SoundList.objects.create(creator=instance, type=SoundList.MAIN, name="Основной список", order=0)

    def is_item_in_list(self, item_id):
        return self.playlist.filter(pk=item_id).exists()

    def is_not_empty(self):
        query = Q(list=self)
        query.add(~Q(type__contains="_"), Q.AND)
        return self.playlist.filter(query).values("pk").exists()

    def get_staff_items(self):
        query = Q(type="PUB")|Q(type="PRI")
        queryset = self.playlist.filter(query)
        return queryset

    def get_items(self):
        query = Q(type="PUB")
        queryset = self.playlist.filter(query)
        return queryset

    def get_penalty_items(self):
        return self.playlist.filter(type__contains="_CLO")

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

    def count_items(self):
        query = Q(type="PUB") | Q(type="MAN")
        return self.playlist.filter(query).values("pk").count()

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
    def is_suspended(self):
        return False
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
        if self.type == "_DEL":
            self.type = SoundList.LIST
        elif self.type == "_DELP":
            self.type = SoundList.PRIVATE
        elif self.type == "_DELM":
            self.type = SoundList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = SoundList.CLOSED
        elif self.type == "MAI":
            self.type = SoundList.CLOSED_MAIN
        elif self.type == "PRI":
            self.type = SoundList.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = SoundList.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = SoundList.LIST
        elif self.type == "_CLOM":
            self.type = SoundList.MAIN
        elif self.type == "_CLOP":
            self.type = SoundList.PRIVATE
        elif self.type == "_CLOMA":
            self.type = SoundList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")

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
        return cls.objects.filter(query)
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(Q(type="MAI")|Q(type="LIS")), Q.AND)
        return cls.objects.filter(query).values("pk").count()
    @classmethod
    def get_user_lists_not_empty(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(Q(type__contains="_")&Q(playlist__isnull=True)), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_user_can_added_list(cls, user_pk):
        from django.conf import settings
        return cls.get_user_lists_count(user_pk) <= settings.USER_MAX_MUSIC_LISTS

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

    @classmethod
    def create_list(cls, creator, name, description, order, community, is_public):
        from notify.models import Notify, Wall
        from common.processing import get_playlist_processing
        if not SoundList.is_user_can_added_list(creator.pk):
            pass
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="MUL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_music_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="MUL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_music_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="MUL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_music_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="MUL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_music_list_notify")
        get_playlist_processing(list, SoundList.LIST)
        return list

    @classmethod
    def create_manager_list(cls, creator, name, description, order):
        from common.processing import get_playlist_processing
        from logs.model.manage_audio import AudioManageLog

        if not order:
            order = 1
        list = cls.objects.create(creator=creator,name=name,description=description,order=order)
        get_playlist_processing(list, SoundList.MANAGER)
        AudioManageLog.objects.create(item=self.pk, manager=creator.pk, action_type=AudioManageLog.LIST_CREATED)
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
            get_playlist_processing(self, SoundList.LIST)
            self.make_publish()
        else:
            get_playlist_processing(self, SoundList.PRIVATE)
            self.make_private()
        return self

    def edit_manager_list(self, name, description, order, manager_id):
        from common.processing import get_playlist_processing
        from logs.model.manage_audio import AudioManageLog

        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        get_playlist_processing(self, SoundList.MANAGER)
        AudioManageLog.objects.create(item=self.pk, manager=manager_id, action_type=AudioManageLog.LIST_EDITED)
        return self


class Music(models.Model):
    PROCESSING, PUBLISHED, PRIVATE, MANAGER, DELETED, CLOSED = '_PRO','PUB','PRI', 'MAN', '_DEL', '_CLO'
    DELETED_PRIVATE, DELETED_MANAGER, CLOSED_PRIVATE, CLOSED_MANAGER = '_DELP', '_DELM', '_CLOP', '_CLOM'
    TYPE = (
        (PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    artwork_url = ProcessedImageField(format='JPEG', blank=True, options={'quality': 100}, upload_to=upload_to_music_directory, processors=[Transpose(), ResizeToFit(width=100, height=100)])
    file = models.FileField(upload_to=upload_to_music_directory, validators=[validate_file_extension], verbose_name="Аудиозапись")
    created = models.DateTimeField(default=timezone.now)
    duration = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    list = models.ManyToManyField(SoundList, related_name='playlist', blank=True)
    media_list = models.ManyToManyField("lists.MediaList", related_name='media_playlist', blank=True, verbose_name="Медиа-список")
    type = models.CharField(max_length=5, choices=TYPE, default=PROCESSING, verbose_name="Тип")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")
    community = models.ForeignKey('communities.Community', related_name='track_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    is_track = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "треки"
        verbose_name_plural = "треки"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ['-created']

    def get_lists(self):
        return self.list.all()

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
        self.type = Music.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Music.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def is_private(self):
        return self.type == self.PRIVATE

    @classmethod
    def create_track(cls, creator, title, file, lists, is_public, community):
        from common.processing import get_music_processing

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового документа")
        private = 0
        track = cls.objects.create(creator=creator,title=title,file=file)
        if community:
            community.plus_tracks(1)
        else:
            creator.plus_tracks(1)
        for list_id in lists:
            track_list = SoundList.objects.get(pk=list_id)
            track_list.playlist.add(track)
            if track_list.is_private():
                private = 1
        if not private and is_public:
            get_music_processing(track, Music.PUBLISHED)
            if community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="MUS", object_id=track.pk, verb="ITE")
                community_send_wall(track.pk, creator.pk, community.pk, None, "create_c_track_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="MUS", object_id=track.pk, verb="ITE")
                    community_send_notify(track.pk, creator.pk, user_id, community.pk, None, "create_c_track_notify")
            else:
                from common.notify.progs import user_send_notify, user_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, type="MUS", object_id=track.pk, verb="ITE")
                user_send_wall(track.pk, None, "create_u_track_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="MUS", object_id=track.pk, verb="ITE")
                    user_send_notify(track.pk, creator.pk, user_id, None, "create_u_track_notify")
        else:
            get_music_processing(track, Music.PRIVATE)
        return track

    @classmethod
    def create_manager_track(cls, creator, title, file, lists):
        from common.processing import get_music_processing
        from logs.model.manage_audio import AudioManageLog
        from lists.models import MediaList

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового элемента")

        track = cls.objects.create(creator=creator,title=title,file=file)
        for list_id in lists:
            list = MediaList.objects.get(pk=list_id)
            track.media_list.add(list)
            list.count += 1
            list.save(update_fields=["count"])
        get_music_processing(track, Music.MANAGER)
        AudioManageLog.objects.create(item=track.pk, manager=creator.pk, action_type=AudioManageLog.ITEM_CREATED)
        return track

    def edit_track(self, title, file, lists, is_public):
        from common.processing import get_music_processing

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового элемента")

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

    def edit_manager_track(self, title, file, lists, manager_id):
        from common.processing import get_track_processing
        from logs.model.manage_track import AudioManageLog

        self.title = title
        self.file = file
        self.lists = lists
        get_track_processing(self, Music.MANAGER)
        AudioManageLog.objects.create(item=self.pk, manager=manager_id, action_type=AudioManageLog.ITEM_EDITED)
        return self.save()

    def delete_track(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Music.DELETED
        elif self.type == "PRI":
            self.type = Music.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = Music.DELETED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_tracks(1)
        else:
            self.creator.minus_tracks(1)
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_track(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Music.PUBLISHED
        elif self.type == "_DELP":
            self.type = Music.PRIVATE
        elif self.type == "_DELM":
            self.type = Music.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_tracks(1)
        else:
            self.creator.plus_tracks(1)
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Music.CLOSED
        elif self.type == "PRI":
            self.type = Music.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = Music.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_tracks(1)
        else:
            self.creator.minus_tracks(1)
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Music.PUBLISHED
        elif self.type == "_CLOP":
            self.type = Music.PRIVATE
        elif self.type == "_CLOM":
            self.type = Music.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_tracks(1)
        else:
            self.creator.plus_tracks(1)
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
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_suspended(self):
        return False
