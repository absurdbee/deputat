import uuid
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from video.helpers import upload_to_video_directory
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
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_user_creator', verbose_name="Создатель")
    type = models.CharField(max_length=5, choices=TYPE, default=PROCESSING, verbose_name="Тип альбома")

    users = models.ManyToManyField("users.User", blank=True, related_name='users_video_album')

    class Meta:
        verbose_name = 'Видеоальбом'
        verbose_name_plural = 'Видеоальбомы'
        ordering = ['order']

    def __str__(self):
        return self.title

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
        if Notify.objects.filter(attach="lvi"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="lvi"+str(self.pk), verb="ITE").update(status="C")
        if Wall.objects.filter(attach="lvi"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="lvi"+str(self.pk), verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = VideoAlbum.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(attach="lvi"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="lvi"+str(self.pk), verb="ITE").update(status="R")
        if Wall.objects.filter(attach="lvi"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="lvi"+str(self.pk), verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        self.type = VideoAlbum.DELETED
        self.save(update_fields=['type'])
        if Notify.objects.filter(attach="lvi"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="lvi"+str(self.pk), verb="ITE").update(status="C")
        if Wall.objects.filter(attach="lvi"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="lvi"+str(self.pk), verb="ITE").update(status="C")
    def abort_delete_list(self):
        from notify.models import Notify, Wall
        self.type = VideoAlbum.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(attach="lvi"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="lvi"+str(self.pk), verb="ITE").update(status="R")
        if Wall.objects.filter(attach="lvi"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="lvi"+str(self.pk), verb="ITE").update(status="R")


class Video(models.Model):
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
    album = models.ManyToManyField(VideoAlbum, related_name="video_album", blank=True, verbose_name="Альбом")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_creator", on_delete=models.CASCADE, verbose_name="Создатель")
    status = models.CharField(choices=STATUS, default=PROCESSING, max_length=3)

    class Meta:
        verbose_name = "Видео-ролики"
        verbose_name_plural = "Видео-ролики"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ['-created']

    def __str__(self):
        return self.title

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
        if Notify.objects.filter(attach="vid"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="vid"+str(self.pk), verb="ITE").update(status="C")
        if Wall.objects.filter(attach="vid"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="vid"+str(self.pk), verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Video.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(attach="vid"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="vid"+str(self.pk), verb="ITE").update(status="R")
        if Wall.objects.filter(attach="vid"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="vid"+str(self.pk), verb="ITE").update(status="R")

    def delete_video(self):
        from notify.models import Notify, Wall
        self.status = Video.DELETED
        self.save(update_fields=['status'])
        if Notify.objects.filter(attach="vid"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="vid"+str(self.pk), verb="ITE").update(status="C")
        if Wall.objects.filter(attach="vid"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="vid"+str(self.pk), verb="ITE").update(status="C")
    def abort_delete_video(self):
        from notify.models import Notify, Wall
        self.status = Video.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(attach="vid"+str(self.pk), verb="ITE").exists():
            Notify.objects.filter(attach="vid"+str(self.pk), verb="ITE").update(status="R")
        if Wall.objects.filter(attach="vid"+str(self.pk), verb="ITE").exists():
            Wall.objects.filter(attach="vid"+str(self.pk), verb="ITE").update(status="R")
