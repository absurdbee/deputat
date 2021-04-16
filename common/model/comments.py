from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from blog.models import Blog, ElectNew
from elect.models import Elect
from users.helpers import upload_to_user_directory
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField


"""
    Группируем все таблицы комментов здесь:
    1. Комменты блога проекта,
    2. Комменты новостей чиновника
"""

class BlogComment(models.Model):
    EDITED = 'EDI'
    DELETED = 'DEL'
    CLOSED = 'CLO'
    PROCESSING = 'PRO'
    PUBLISHED = 'PUB'
    STATUS = (
        (DELETED, 'Удалённый'),
        (EDITED, 'Изменённый'),
        (CLOSED, 'Закрытый менеджером'),
        (PROCESSING, 'Обработка'),
        (PUBLISHED, 'Опубликовано'),
    )
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='blog_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    status = models.CharField(max_length=5, choices=STATUS, default=PROCESSING, verbose_name="Тип альбома")

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name = "комментарий к статье"
        verbose_name_plural = "комментарии к статье"
        ordering = ["-created"]

    def __str__(self):
        if self.text:
            return self.text[:10]
        else:
            return 'Комментатор ' + str(self.commenter)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        return BlogComment.objects.filter(parent=self,status=BlogComment.PUBLISHED).only("pk")

    def count_replies(self):
        return self.get_replies().count()

    def likes(self):
        from common.model.votes import BlogCommentVotes
        return BlogCommentVotes.objects.filter(comment_id=self.pk, vote__gt=0)

    def likes_count(self):
        from common.model.votes import BlogCommentVotes
        return BlogCommentVotes.objects.filter(comment_id=self.pk, vote__gt=0).values("pk").count()

    def dislikes_count(self):
        from common.model.votes import BlogCommentVotes
        return BlogCommentVotes.objects.filter(comment_id=self.pk, vote__lt=0).values("pk").count()

    def dislikes(self):
        from common.model.votes import BlogCommentVotes
        dislikes = BlogCommentVotes.objects.filter(comment_id=self.pk, vote__lt=0)
        return dislikes

    def likes_count(self):
        from common.model.votes import BlogCommentVotes
        likes = BlogCommentVotes.objects.filter(comment_id=self.pk, vote__gt=0).values("pk")
        count = likes.count()
        if count:
            return count
        else:
            return ''

    def dislikes_count(self):
        from common.model.votes import BlogCommentVotes
        dislikes = BlogCommentVotes.objects.filter(comment_id=self.pk, vote__lt=0).values("pk")
        count = dislikes.count()
        if count:
            return count
        else:
            return ''

    @classmethod
    def create_comment(cls, commenter, blog, parent, text, attach):
        from common.notify import user_wall, user_notify
        from django.utils import timezone
        from common.processing import get_blog_message_processing
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")

        if text or _attach:
            comment = BlogComment.objects.create(commenter=commenter, parent=parent, blog=blog, text=text, attach=_attach, created=timezone.now())
            if parent:
                blog = parent.blog
                type = "blr"+str(comment.pk)+",blc"+str(parent.pk)+",blo"+str(blog.pk)
                user_wall(commenter, type, "u_blog_comment_notify", "REP")
                user_notify(commenter, type, "u_blog_comment_notify", "REP")
            else:
                type = "blc"+str(comment.pk)+", blo"+str(blog.pk)
                user_wall(commenter, type, "u_blog_comment_notify", "COM")
                user_notify(commenter, type, "u_blog_comment_notify", "COM")

            get_blog_message_processing(comment)
            return comment
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Нужно написать текст, вставить картинку или документ")

    def count_replies_ru(self):
        count = self.get_replies().count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"

    def get_u_attach(self, user):
        from common.attach.comment_attach import get_u_blog_comment_attach
        return get_u_blog_comment_attach(self, user)

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


class ElectNewComment(models.Model):
    EDITED = 'EDI'
    DELETED = 'DEL'
    CLOSED = 'CLO'
    PROCESSING = 'PRO'
    PUBLISHED = 'PUB'
    STATUS = (
        (DELETED, 'Удалённый'),
        (EDITED, 'Изменённый'),
        (CLOSED, 'Закрытый менеджером'),
        (PROCESSING, 'Обработка'),
        (PUBLISHED, 'Опубликовано'),
    )
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='elect_new_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    new = models.ForeignKey(ElectNew, on_delete=models.CASCADE, blank=True, null=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    status = models.CharField(max_length=5, choices=STATUS, default=PROCESSING, verbose_name="Тип альбома")

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name = "комментарий к новости депутата"
        verbose_name_plural = "комментарии к новости депутата"
        ordering = ["-created"]

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        get_comments = ElectNewComment.objects.filter(parent=self).all()
        return get_comments

    def count_replies(self):
        return BlogComment.objects.filter(parent=self,type=ElectNewComment.PUBLISHED).only("pk")

    def likes(self):
        from common.model.votes import ElectNewCommentVotes
        return ElectNewCommentVotes.objects.filter(comment_id=self.pk, vote__gt=0)

    def likes_count(self):
        from common.model.votes import ElectNewCommentVotes
        return ElectNewCommentVotes.objects.filter(comment_id=self.pk, vote__gt=0).values("pk").count()

    def dislikes_count(self):
        from common.model.votes import ElectNewCommentVotes
        return ElectNewCommentVotes.objects.filter(comment_id=self.pk, vote__lt=0).values("pk").count()

    def dislikes(self):
        from common.model.votes import ElectNewCommentVotes
        return ElectNewCommentVotes.objects.filter(comment_id=self.pk, vote__lt=0)

    def likes_count(self):
        from common.model.votes import ElectNewCommentVotes
        likes = ElectNewCommentVotes.objects.filter(comment_id=self.pk, vote__gt=0).values("pk")
        count = likes.count()
        if count:
            return count
        else:
            return ''

    def dislikes_count(self):
        from common.model.votes import ElectNewCommentVotes
        dislikes = ElectNewCommentVotes.objects.filter(comment_id=self.pk, vote__lt=0).values("pk")
        count = dislikes.count()
        if count:
            return count
        else:
            return ''

    @classmethod
    def create_comment(cls, commenter, new=None, parent=None, text=None, created=None ):
        comment = ElectNewComment.objects.create(commenter=commenter, parent=parent, new=new, text=text)
        comment.save()
        return comment

    def count_replies_ru(self):
        count = self.get_replies().count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"

    def get_u_attach(self, user):
        from common.attach.comment_attach import get_u_elect_new_comment_attach
        return get_u_elect_new_comment_attach(self, user)

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
