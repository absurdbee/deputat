from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q
from ckeditor_uploader.fields import RichTextUploadingField
from users.helpers import upload_to_user_directory
from taggit.managers import TaggableManager
from elect.models import Elect
from lists.models import ElectNewsCategory
from autoslug import AutoSlugField

"""
    Группируем все таблицы новостей здесь:
    1. Новости всего проекта,
    2. Лента депутата - его высказывания, выборы, работа с избирателями
"""


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 90}, upload_to="blog/%Y/%m/%d/", processors=[ResizeToFit(width=1600, upscale=False)], verbose_name="Главное изображение")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    content = RichTextUploadingField(config_name='default',)
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name="Создатель")
    slug = AutoSlugField(populate_from='title', null=True)

    comment = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    inert = models.PositiveIntegerField(default=0, verbose_name="Кол-во inert")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        verbose_name = "Новость проекта"
        verbose_name_plural = "Новости проекта"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-created"]

    def __str__(self):
        return self.title

    @classmethod
    def create_new(cls, creator, description, content, comments_enabled, votes_on, status):
        from notify.models import Notify

        blog = cls.objects.create(creator=creator,description=description,category=category,comments_enabled=comments_enabled,votes_on=votes_on,status=Blog.STATUS_DRAFT,)
        Notify.objects.create(creator_id=creator.pk, type="BLO", object_id=blog.pk, verb="ITE")
        return blog

    def likes(self):
        from common.model.votes import BlogVotes
        return BlogVotes.objects.filter(blog_id=self.pk, vote="LIK")
    def dislikes(self):
        from common.model.votes import BlogVotes
        return BlogVotes.objects.filter(blog_id=self.pk, vote="DIS")
    def inerts(self):
        from common.model.votes import BlogVotes
        return BlogVotes.objects.filter(blog_id=self.pk, vote="INE")

    def is_have_likes(self):
        return self.like > 0
    def is_have_dislikes(self):
        return self.dislike > 0
    def is_have_inerts(self):
        return self.inert > 0

    def likes_count(self):
        if self.like > 0:
            return self.like > 0
        else:
            return ''
    def dislikes_count(self):
        if self.dislike > 0:
            return self.like > 0
        else:
            return ''
    def inerts_count(self):
        if self.inert > 0:
            return self.like > 0
        else:
            return ''

    def count_comments(self):
        if self.comment > 0:
            return self.comment > 0
        else:
            return ''

    def count_reposts(self):
        if self.repost > 0:
            return self.repost > 0
        else:
            return ''

    def get_comments(self):
        from common.model.comments import BlogComment

        comments_query = Q(blog_id=self.pk, status=BlogComment.PUBLISHED, parent__isnull=True)
        return BlogComment.objects.filter(comments_query)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def visits_count(self):
        return self.view

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/static/images/no_photo.jpg'

    def get_manager_tags(self):
        from tags.models import ManagerTag
        tags = ManagerTag.objects.filter(blog=self).values("name")
        return [i['name'] for i in tags]

    def count_views(self):
        from stst.models import BlogNumbers
        return BlogNumbers.objects.filter(new=self.pk).values("pk").count()

    def is_blog_in_bookmarks(self, user_id):
        from users.model.profile import Bookmarks
        return Bookmarks.objects.filter(blog=self, user_id=user_id).exists()

    def get_attach_photos(self):
        if "pho" in self.attach:
            query = []
            from gallery.models import Photo

            for item in self.attach.split(","):
                if item[:3] == "pho":
                    query.append(item[3:])
        return Photo.objects.filter(id__in=query)

    def get_attach_videos(self):
        if "pho" in self.attach:
            query = []
            from video.models import Video

            for item in self.attach.split(","):
                if item[:3] == "vid":
                    query.append(item[3:])
        return Video.objects.filter(id__in=query)


class ElectNew(models.Model):
    DRAFT = '_DRA'
    PROCESSING = '_PRO'
    SUGGESTED = '_SUG'
    PUBLISHED = 'PUB'
    DELETED = '_DEL'
    CLOSED = '_CLO'
    MANAGER = 'MAN'
    STATUSES = (
        (DRAFT, 'Черновик'),
        (PROCESSING, 'В процессе'),
        (PUBLISHED, 'Опубликованый'),
        (DELETED, 'Удаленый'),
        (CLOSED, 'Закрытый'),
        (MANAGER, 'Менеджерский'),
        (SUGGESTED, 'Предложенный'),
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    elect = models.ForeignKey(Elect, on_delete=models.SET_NULL, blank=True, null=True, related_name="new_elect", verbose_name="Чиновник")
    category = models.ForeignKey(ElectNewsCategory, on_delete=models.SET_NULL, related_name="elect_cat", blank=True, null=True, verbose_name="Категория активности")
    status = models.CharField(choices=STATUSES, default=PROCESSING, max_length=5, verbose_name="Статус записи")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="elect_new_creator", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Создатель")
    content = RichTextUploadingField(config_name='default',)
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")

    comment = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    inert = models.PositiveIntegerField(default=0, verbose_name="Кол-во inert")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        verbose_name = "Активность"
        verbose_name_plural = "Лента чиновника"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-created"]

    def __str__(self):
        return self.title

    @classmethod
    def create_suggested_new(cls, creator, description, category, comments_enabled, votes_on, status):
        from common.notify import user_wall, user_notify

        elect_new = cls.objects.create(creator=creator,description=description,category=category,comments_enabled=comments_enabled,votes_on=votes_on,status=ElectNew.SUGGESTED,)
        user_wall(creator, "ELN", elect_new.pk, "draft_news_wall", "SIT")
        user_notify(creator, "ELN", elect_new.pk, "draft_news_notify", "SIT")
        return elect_new

    def make_publish_new(self):
        from common.notify import user_wall, user_notify

        self.status = ElectNew.PUBLISHED
        self.save(update_fields=['status'])
        user_wall(self.manager, "ELN", elect_new.pk, "news_wall", "ITE")
        user_notify(self.manager, "ELN", elect_new.pk, "news_notify", "ITE")
        return self

    def is_draft(self):
        return self.status == ElectNew.DRAFT
    def is_published(self):
        return self.status == ElectNew.PUBLISHED
    def is_manager(self):
        return self.status == ElectNew.MANAGER
    def is_suggested(self):
        return self.status == ElectNew.SUGGESTED
    def is_deleted(self):
        return self.status == ElectNew.DELETED
    def is_suggested(self):
        return self.status == ElectNew.SUGGESTED

    def likes(self):
        from common.model.votes import ElectNewVotes2
        return ElectNewVotes2.objects.filter(new_id=self.pk, vote="LIK")
    def dislikes(self):
        from common.model.votes import ElectNewVotes2
        return ElectNewVotes2.objects.filter(new_id=self.pk, vote="DIS")
    def inerts(self):
        from common.model.votes import ElectNewVotes2
        return ElectNewVotes2.objects.filter(new_id=self.pk, vote="INE")

    def is_have_likes(self):
        return self.like > 0
    def is_have_dislikes(self):
        return self.dislike > 0
    def is_have_inerts(self):
        return self.inert > 0

    def likes_count(self):
        if self.like > 0:
            return self.like > 0
        else:
            return ''
    def dislikes_count(self):
        if self.dislike > 0:
            return self.like > 0
        else:
            return ''
    def inerts_count(self):
        if self.inert > 0:
            return self.like > 0
        else:
            return ''

    def count_reposts(self):
        if self.repost > 0:
            return self.repost > 0
        else:
            return ''

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def visits_count(self):
        return self.view

    def get_image_url(self):
        return self.creator.s_avatar.url

    def count_comments(self):
        if self.comment > 0:
            return self.comment > 0
        else:
            return ''

    def get_comments(self):
        from common.model.comments import ElectNewComment
        return ElectNewComment.objects.filter(new_id=self.pk, parent__isnull=True)

    def get_attach_photos(self):
        if "pho" in self.attach:
            query = []
            from gallery.models import Photo

            for item in self.attach.split(","):
                if item[:3] == "pho":
                    query.append(item[3:])
        return Photo.objects.filter(id__in=query)

    def get_attach_videos(self):
        if "pho" in self.attach:
            query = []
            from video.models import Video

            for item in self.attach.split(","):
                if item[:3] == "vid":
                    query.append(item[3:])
        return Video.objects.filter(id__in=query)
