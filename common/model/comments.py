from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from blog.models import Blog, ElectNew
from elect.models import Elect


"""
    Группируем все таблицы комментов здесь:
    1. Комменты блога проекта,
    2. Комменты новостей чиновника
    3. Отзывы о чиновнике
"""

class BlogComment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='blog_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False, verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False, verbose_name="Удаено")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name = "комментарий к статье"
        verbose_name_plural = "комментарии к статье"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        get_comments = BlogComment.objects.filter(parent=self).all()
        return get_comments

    def count_replies(self):
        return self.blog_comment_replies.count()

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
    def create_comment(cls, commenter, blog=None, parent=None, text=None, created=None):
        comment = BlogComment.objects.create(commenter=commenter, parent=parent, blog=blog, text=text)
        comment.save()
        return comment

    def count_replies_ru(self):
        count = self.blog_comment_replies.count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"


class ElectNewComment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='elect_new_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False, verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False, verbose_name="Удаено")
    new = models.ForeignKey(ElectNew, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name = "комментарий к новости депутата"
        verbose_name_plural = "комментарии к новости депутата"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        get_comments = ElectNewComment.objects.filter(parent=self).all()
        return get_comments

    def count_replies(self):
        return self.elect_new_comment_replies.count()

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
        count = self.elect_new_comment_replies.count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"


class ElectComment(models.Model):
    from elect.models import Elect

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='elect_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False, verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False, verbose_name="Удаено")
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name = "отзыв о депутате"
        verbose_name_plural = "отзывы о депутате"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        get_comments = ElectComment.objects.filter(parent=self).all()
        return get_comments

    def count_replies(self):
        return self.elect_comment_replies.count()

    def likes(self):
        from common.model.votes import ElectCommentVotes
        return ElectCommentVotes.objects.filter(comment_id=self.pk, vote__gt=0)

    def likes_count(self):
        from common.model.votes import ElectCommentVotes
        return ElectCommentVotes.objects.filter(comment_id=self.pk, vote__gt=0).values("pk").count()

    def dislikes_count(self):
        from common.model.votes import ElectCommentVotes
        return ElectCommentVotes.objects.filter(comment_id=self.pk, vote__lt=0).values("pk").count()

    def dislikes(self):
        from common.model.votes import ElectCommentVotes
        return ElectCommentVotes.objects.filter(comment_id=self.pk, vote__lt=0)

    def likes_count(self):
        from common.model.votes import ElectCommentVotes
        likes = ElectCommentVotes.objects.filter(comment_id=self.pk, vote__gt=0).values("pk")
        count = likes.count()
        if count:
            return count
        else:
            return ''

    def dislikes_count(self):
        from common.model.votes import ElectCommentVotes
        dislikes = ElectCommentVotes.objects.filter(comment_id=self.pk, vote__lt=0).values("pk")
        count = dislikes.count()
        if count:
            return count
        else:
            return ''

    @classmethod
    def create_comment(cls, commenter, elect=None, parent=None, text=None, created=None ):
        comment = ElectComment.objects.create(commenter=commenter, parent=parent, elect=elect, text=text)
        comment.save()
        return comment

    def count_replies_ru(self):
        count = self.elect_comment_replies.count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"
