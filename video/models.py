import uuid
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from video.helpers import upload_to_video_directory, validate_file_extension
from django.db.models import Q
from communities.models import Community
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class VideoList(models.Model):
    MAIN, LIST, MANAGER, PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI'
    DELETED, DELETED_PRIVATE, DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    CLOSED, CLOSED_PRIVATE, CLOSED_MAIN, CLOSED_MANAGER = '_CLO', '_CLOP', '_CLOM', '_CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PROCESSING, 'Обработка'),
        (DELETED, 'Удалённый'),(DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    name = models.CharField(max_length=250, verbose_name="Название")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_list_creator', verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=PROCESSING, verbose_name="Тип альбома")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
    community = models.ForeignKey('communities.Community', related_name='video_lists_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    class Meta:
        verbose_name = 'Видеоальбом'
        verbose_name_plural = 'Видеоальбомы'
        ordering = ['order']

    def __str__(self):
        return self.name

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            VideoList.objects.create(community=instance, type=VideoList.MAIN, name="Основной список", order=0, creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            VideoList.objects.create(creator=instance, type=VideoList.MAIN, name="Основной список", order=0)

    @classmethod
    def create_list(cls, creator, name, description, order, community, is_public):
        from notify.models import Notify, Wall
        from common.processing import get_video_list_processing
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="VIL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_video_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="VIL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_video_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="VIL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_video_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="VIL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_video_list_notify")
        get_video_list_processing(list, VideoList.LIST)
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
            get_video_list_processing(self, VideoList.LIST)
            self.make_publish()
        else:
            get_video_list_processing(self, VideoList.PRIVATE)
            self.make_private()
        return self

    def count_items(self):
        return self.video_list.filter(type="PUB").values("pk").count()

    def get_staff_items(self):
        query = Q(type="PUB") | Q(type="PRI")
        return self.video_list.filter(query)

    def get_items(self):
        query = Q(type="PUB")
        queryset = self.video_list.filter(type="PUB")
        return queryset

    def get_penalty_items(self):
        return self.video_list.filter(type__contains="_CLO")

    def get_video_count(self):
        query = Q(type="PUB") | Q(type="PRI")
        return self.video_list.filter(query).values("pk").count()

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


    def is_not_empty(self):
        query = Q(list=self)
        query.add(~Q(type__contains="_"), Q.AND)
        return self.video_list.filter(query).exists()

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

    def is_item_in_list(self, item_id):
        return self.video_list.filter(pk=item_id).exists()

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = VideoList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = VideoList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = VideoList.DELETED
        elif self.type == "PRI":
            self.type = VideoList.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = VideoList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = VideoList.LIST
        elif self.type == "_DELP":
            self.type = VideoList.PRIVATE
        elif self.type == "_DELM":
            self.type = VideoList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = VideoList.CLOSED
        elif self.type == "MAI":
            self.type = VideoList.CLOSED_MAIN
        elif self.type == "PRI":
            self.type = VideoList.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = VideoList.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = VideoList.LIST
        elif self.type == "_CLOM":
            self.type = VideoList.MAIN
        elif self.type == "_CLOP":
            self.type = VideoList.PRIVATE
        elif self.type == "_CLOMA":
            self.type = VideoList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")

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
        query.add(~Q(video_list__isnull=False), Q.AND)
        return cls.objects.filter(query)

    @classmethod
    def get_community_staff_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(~Q(type__contains="_"), Q.AND)
        query.add(~Q(Q(type="MAI")&Q(community_id=community_pk)), Q.AND)
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


class Video(models.Model):
    PROCESSING, PUBLISHED, PRIVATE, MANAGER, DELETED, CLOSED = 'PRO','PUB','PRI', 'MAN', 'DEL', 'CLO'
    DELETED_PRIVATE, DELETED_MANAGER, CLOSED_PRIVATE, CLOSED_MANAGER = 'DELP', 'DELM', 'CLOP', 'CLOM'
    TYPE = (
        (PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )

    image = ProcessedImageField(format='JPEG',
                                options={'quality': 90},
                                upload_to=upload_to_video_directory,
                                processors=[ResizeToFit(width=500, upscale=False)],
                                verbose_name="Обложка",blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    category = models.ForeignKey(VideoCategory, blank=True, null=True, related_name='video_category', on_delete=models.CASCADE, verbose_name="Категория")
    title = models.CharField(max_length=255, verbose_name="Название")
    uri = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ссылка на видео")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    list = models.ManyToManyField(VideoList, related_name="video_list", blank=True, verbose_name="Альбом")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_creator", on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(choices=TYPE, default=PROCESSING, max_length=5)
    file = models.FileField(upload_to=upload_to_video_directory, blank=True, null=True, validators=[validate_file_extension], verbose_name="Видеозапись")
    community = models.ForeignKey('communities.Community', related_name='video_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    class Meta:
        verbose_name = "Видео-ролики"
        verbose_name_plural = "Видео-ролики"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ['-created']

    def __str__(self):
        return self.title

    @classmethod
    def create_video(cls, creator, title, file, image, uri, lists, is_public, community):
        from common.processing import get_video_processing

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового документа")
        elif not file and not uri:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран файл для ссылка")
        if uri:
            current_uri = uri.replace("watch?v=", "embed/")
        else:
            current_uri = ""
        private = 0
        video = cls.objects.create(creator=creator,title=title,image=image,file=file,uri=current_uri,community=community)
        if community:
            community.plus_videos(1)
        else:
            creator.plus_videos(1)
        for list_id in lists:
            video_list = VideoList.objects.get(pk=list_id)
            video_list.video_list.add(video)
            if video_list.is_private():
                private = 1
        if not private and is_public:
            get_video_processing(video, Video.PUBLISHED)
            if community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                community_send_wall(video.pk, creator.pk, community.pk, None, "create_c_video_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                    community_send_notify(video.pk, creator.pk, user_id, community.pk, None, "create_c_video_notify")
            else:
                from common.notify.progs import user_send_notify, user_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, type="VID", object_id=video.pk, verb="ITE")
                user_send_wall(video.pk, None, "create_u_video_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                    user_send_notify(video.pk, creator.pk, user_id, None, "create_u_video_notify")
        else:
            get_video_processing(video, Video.PRIVATE)
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

    def get_lists_for_video(self):
        return self.list.all()
    def get_list_uuid(self):
        return self.list.all()[0].uuid

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = Video.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Video.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def delete_video(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Video.DELETED
        elif self.type == "PRI":
            self.type = Video.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = Video.DELETED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_videos(1)
        else:
            self.creator.minus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_video(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Video.PUBLISHED
        elif self.type == "_DELP":
            self.type = Video.PRIVATE
        elif self.type == "_DELM":
            self.type = Video.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_videos(1)
        else:
            self.creator.plus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Video.CLOSED
        elif self.type == "PRI":
            self.type = Video.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = Video.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_videos(1)
        else:
            self.creator.minus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Video.PUBLISHED
        elif self.type == "_CLOP":
            self.type = Video.PRIVATE
        elif self.type == "_CLOM":
            self.type = Video.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_videos(1)
        else:
            self.creator.plus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

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

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return "/static/images/list.jpg"

    def get_lists(self):
        return self.list.all()

    def get_list_uuid(self):
        return self.list.all()[0].uuid
