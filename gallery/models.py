import uuid
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q
from django.conf import settings
from gallery.helpers import upload_to_photo_directory
from django.utils import timezone


class Album(models.Model):
    MAIN = 'MAI'
    LIST = 'LIS'
    DELETED = 'DEL'
    PRIVATE = 'PRI'
    CLOSED = 'CLO'
    MANAGER = 'MAN'
    TYPE = (
        (MAIN, 'Фото со стены'),
        (LIST, 'Пользовательский'),
        (DELETED, 'Удалённый'),
        (PRIVATE, 'Приватный'),
        (CLOSED, 'Закрытый менеджером'),
        (MANAGER, 'Созданный персоналом'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    cover_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, related_name='+', blank=True, null=True, verbose_name="Обожка")
    type = models.CharField(max_length=5, choices=TYPE, default=LIST, verbose_name="Тип альбома")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_album_creator', null=False, blank=False, verbose_name="Создатель")

    users = models.ManyToManyField("users.User", blank=True, related_name='users_photolist')

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'

    def __str__(self):
        return self.title

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

    def is_main_album(self):
        return self.type == self.MAIN
    def is_user_album(self):
        return self.type == self.LIST or self.type == self.PRIVATE
    def is_private_album(self):
        return self.type == self.PRIVATE

    def get_cover_photo(self):
        if self.cover_photo:
            return self.cover_photo.file.url
        elif self.photo_album.filter(type="PUB").exists():
            return self.photo_album.filter(type="PUB").last().file.url
        else:
            return "/static/images/album.jpg"

    def get_first_photo(self):
        return self.photo_album.filter(type="PUB").first()

    def count_photo(self):
        try:
            return self.photo_album.filter(type="PUB").values("pk").count()
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
        return self.photo_album.filter(type="PUB")

    def get_staff_photos(self):
        query = Q(type="PUB") | Q(type="PRI")
        return self.photo_album.filter(query)

    def is_not_empty(self):
        return self.photo_album.filter(album=self, type="PUB").values("pk").exists()

    def is_photo_in_album(self, photo_id):
        return self.photo_album.filter(pk=photo_id).values("pk").exists()


class Photo(models.Model):
    PROCESSING = 'PRO'
    PUBLISHED = 'PUB'
    DELETED = 'DEL'
    PRIVATE = 'PRI'
    CLOSED = 'CLO'
    MANAGER = 'MAN'
    TYPE = (
        (PROCESSING, 'Обработка'),
        (PUBLISHED, 'Опубликовано'),
        (DELETED, 'Удалено'),
        (PRIVATE, 'Приватно'),
        (CLOSED, 'Закрыто модератором'),
        (MANAGER, 'Созданный персоналом'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    album = models.ManyToManyField(Album, related_name="photo_album", blank=True)
    file = ProcessedImageField(format='JPEG', options={'quality': 100}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=1024, upscale=False)])
    preview = ProcessedImageField(format='JPEG', options={'quality': 60}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=102, upscale=False)])
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_creator', null=False, blank=False, verbose_name="Создатель")
    type = models.CharField(max_length=5, choices=TYPE, default=PROCESSING, verbose_name="Тип альбома")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ["-created"]

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    @classmethod
    def create_photo(cls, creator, album=None, file=None, created=None, is_public=None):
        photo = Photo.objects.create(creator=creator, file=file, is_public=is_public, album=album)
        return photo

    def is_album_exists(self):
        return self.photo_album.filter(creator=self.creator).exists()

    def delete_photo(self):
        try:
            from notify.models import Notify
            Notify.objects.filter(attach="pho" + str(self.pk)).update(status="C")
        except:
            pass
        self.type = "DEL"
        return self.save(update_fields=['type'])

    def abort_delete_photo(self):
        try:
            from notify.models import Notify
            Notify.objects.filter(attach="pho" + str(self.pk)).update(status="R")
        except:
            pass
        self.type = "PUB"
        return self.save(update_fields=['type'])

    def get_type(self):
        return self.album.all()[0].type

    def is_private(self):
        return self.type == self.PRIVATE
