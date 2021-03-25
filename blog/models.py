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
    tags = TaggableManager(blank=True, verbose_name="Теги")
    slug = AutoSlugField(populate_from='title', null=True)

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
        Notify.objects.create(creator_id=creator.pk, attach="blo"+str(blog.pk), verb="ITE")
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
        from common.model.votes import BlogVotes
        return BlogVotes.objects.filter(blog_id=self.pk, vote="LIK").exists()
    def is_have_dislikes(self):
        from common.model.votes import BlogVotes
        return BlogVotes.objects.filter(blog_id=self.pk, vote="DIS").exists()
    def is_have_inerts(self):
        from common.model.votes import BlogVotes
        return BlogVotes.objects.filter(blog_id=self.pk, vote="INE").exists()

    def likes_count(self):
        from common.model.votes import BlogVotes
        likes = BlogVotes.objects.filter(blog_id=self.pk, vote="LIK").values("pk")
        count = likes.count()
        if count:
            return count
        else:
            return ''
    def dislikes_count(self):
        from common.model.votes import BlogVotes
        dislikes = BlogVotes.objects.filter(blog_id=self.pk, vote="DIS").values("pk")
        count = dislikes.count()
        if count:
            return count
        else:
            return ''
    def inerts_count(self):
        from common.model.votes import BlogVotes
        inerts = BlogVotes.objects.filter(blog_id=self.pk, vote="INE").values("pk")
        count = inerts.count()
        if count:
            return count
        else:
            return ''

    def reposts_count(self):
        return ''

    def count_comments(self):
        from common.model.comments import BlogComment

        parent_comments = BlogComment.objects.filter(blog_id=self.pk)
        parents_count = parent_comments.count()
        i = 0
        for comment in parent_comments:
            i = i + comment.count_replies()
        i = i + parents_count
        if i == 0:
            return ''
        else:
            return i

    def get_comments(self):
        from common.model.comments import BlogComment

        comments_query = Q(blog_id=self.pk)
        comments_query.add(Q(parent__isnull=True), Q.AND)
        return BlogComment.objects.filter(comments_query)

    def get_articles_5(self):
        return Blog.objects.filter(category__in=self.category.all())[:5]

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def visits_count(self):
        from stst.models import BlogNumbers
        return BlogNumbers.objects.filter(new=self.pk).values('pk').count()

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
        from user.model.profile import Bookmarks
        return Bookmarks.objects.filter(blog=self, user_id=user_id).exists()


class ElectNew(models.Model):
    STATUS_DRAFT = 'D'
    STATUS_PROCESSING = 'PG'
    STATUS_PUBLISHED = 'P'
    STATUSES = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_PUBLISHED, 'Опубликовано'),
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    elect = models.ManyToManyField(Elect, related_name="new_elect", blank=True, verbose_name="Чиновник")
    category = models.ForeignKey(ElectNewsCategory, on_delete=models.CASCADE, related_name="elect_cat", blank=True, null=True, verbose_name="Категория активности")
    status = models.CharField(blank=False, null=False, choices=STATUSES, default=STATUS_PUBLISHED, max_length=2, verbose_name="Статус записи")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Создатель")
    content = RichTextUploadingField(config_name='default',)
    tags = TaggableManager(blank=True, verbose_name="Теги")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")

    class Meta:
        verbose_name = "Активность"
        verbose_name_plural = "Лента чиновника"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-created"]

    def __str__(self):
        return self.title

    @classmethod
    def create_draft_post(cls, creator, description, category, comments_enabled, votes_on, status):
        from notify.models import Notify

        elect_new = cls.objects.create(creator=creator,description=description,category=category,comments_enabled=comments_enabled,votes_on=votes_on,status=ElectNew.STATUS_DRAFT,)
        Notify.objects.create(creator_id=creator.pk, attach="new"+str(elect_new.pk), verb="SIT")
        return elect_new

    def make_publishe_post(self):
        from notify.models import Notify

        self.status = ElectNew.STATUS_PUBLISHED
        self.save(update_fields=['status'])
        try:
            old_notify = Notify.objects.get(creator_id=self.creator.pk, attach="new"+str(self.pk), verb="SIT")
            old_notify.delete()
        except Notify.DoesNotExist:
            pass
        Notify.objects.create(creator_id=self.creator.pk, attach="new"+str(self.pk), verb="ITE")

    def is_draft(self):
        return self.status == ElectNew.STATUS_DRAFT

    def is_published(self):
        return self.status == ElectNew.STATUS_PUBLISHED

    def likes(self):
        from common.model.votes import ElectNewVotes2
        return ElectNewVotes2.objects.filter(new_id=self.pk, vote__gt=0)

    def dislikes(self):
        from common.model.votes import ElectNewVotes2
        return ElectNewVotes2.objects.filter(new_id=self.pk, vote__lt=0)

    def likes_count(self):
        from common.model.votes import ElectNewVotes2
        likes = ElectNewVotes2.objects.filter(new_id=self.pk, vote__gt=0).values("pk")
        count = likes.count()
        if count:
            return count
        else:
            return ''

    def dislikes_count(self):
        from common.model.votes import ElectNewVotes2
        dislikes = ElectNewVotes2.objects.filter(new_id=self.pk, vote__lt=0).values("pk")
        count = dislikes.count()
        if count:
            return count
        else:
            return ''

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def visits_count(self):
        from stst.models import ElectNewNumbers
        return ElectNewNumbers.objects.filter(new=self.pk).values('pk').count()

    def is_have_docs(self):
        if self.doc_new.filter(new_id=self.pk).exists():
            return True
        else:
            return False

    def is_have_images(self):
        if self.image_new.filter(new_id=self.pk).exists():
            return True
        else:
            return False

    def get_docs(self):
        return self.doc_new.filter(new_id=self.pk)

    def get_images(self):
        return self.image_new.filter(new_id=self.pk)

    def get_elects(self):
        return self.elect.all()

    def get_image_url(self):
        return self.image_new.filter(new_id=self.pk)[0].file.url

    def count_comments(self):
        from common.model.comments import ElectNewComment

        comments = ElectNewComment.objects.filter(new_id=self.pk)
        parents_count = comments.count()
        i = 0
        for comment in comments:
            i = i + comment.count_replies()
        i = i + parents_count
        return i

    def get_comments(self):
        from common.model.comments import ElectNewComment

        comments_query = Q(new_id=self.pk)
        comments_query.add(Q(parent__isnull=True), Q.AND)
        return ElectNewComment.objects.filter(comments_query)


class ElectDoc(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to=upload_to_user_directory, verbose_name="Документ")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_creator', null=False, blank=False, verbose_name="Создатель")
    new = models.ForeignKey(ElectNew, related_name='doc_new', on_delete=models.CASCADE, blank=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        indexes = (BrinIndex(fields=['created']),)

    def get_mime_type(self):
        import magic
        return magic.from_file(self.file.path, mime=True)


class ElectPhoto(models.Model):
    file = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to=upload_to_user_directory, processors=[Transpose(), ResizeToFit(width=1024, upscale=False)])
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_creator', null=False, blank=False, verbose_name="Создатель")
    new = models.ForeignKey(ElectNew, related_name='image_new', on_delete=models.CASCADE, blank=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ["-created"]
