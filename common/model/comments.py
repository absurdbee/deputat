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
    def create_comment(cls, commenter, blog, parent, text, files, images):
        from common.notify import user_wall, user_notify

        if not text:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Нужно написать текст, вставить картинку или документ")
        comment = BlogComment.objects.create(commenter=commenter, parent=parent, blog=blog, text=text, created=timezone.now())
        if parent:
            blog = parent.blog
            type = "blr"+str(comment.pk)+",blc"+str(parent.pk)+",blo"+str(blog.pk)
            user_wall(commenter, None, type, "u_blog_comment_notify", "REP")
            user_notify(commenter, blog.creator.pk, None, type, "u_blog_comment_notify", "REP")
        else:
            type = "blc"+str(comment.pk)+", bls"+str(blog.pk)
            user_wall(commenter, None, type, "u_blog_comment_notify", "COM")
            user_notify(commenter, blog.creator.pk, None, type, "u_blog_comment_notify", "COM")
        if files:
            for file in files:
                BlogCommentDoc.objects.create(comment=comment, file=file)
        if images:
            for image in images:
                BlogCommentPhoto.objects.create(comment=comment, file=file)
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

    def is_have_docs(self):
        return self.blog_comment_doc.filter(comment_id=self.pk).exists()

    def is_have_images(self):
        return self.blog_comment_image.filter(comment_id=self.pk).exists()

    def get_docs(self):
        return self.blog_comment_doc.filter(comment_id=self.pk)

    def get_images(self):
        return self.blog_comment_image.filter(comment_id=self.pk)

class BlogCommentDoc(models.Model):
    file = models.FileField(upload_to=upload_to_user_directory, verbose_name="Документ")
    comment = models.ForeignKey(BlogComment, related_name='blog_comment_doc', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = "Документ коммента к статье блога"
        verbose_name_plural = "Документы коммента к статье блога"

class BlogCommentPhoto(models.Model):
    file = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to=upload_to_user_directory, processors=[Transpose(), ResizeToFit(width=1024, upscale=False)])
    comment = models.ForeignKey(BlogComment, related_name='blog_comment_image', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Фото коммента к статье блога'
        verbose_name_plural = 'Фото коммента к статье блога'


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

    def is_have_docs(self):
        return self.elect_new_comment_doc.filter(comment_id=self.pk).exists()

    def is_have_images(self):
        return self.elect_new_comment_photo.filter(comment_id=self.pk).exists()

    def get_docs(self):
        return self.elect_new_comment_doc.filter(comment_id=self.pk)

    def get_images(self):
        return self.elect_new_comment_photo.filter(comment_id=self.pk)

class ElectNewCommentDoc(models.Model):
    file = models.FileField(upload_to=upload_to_user_directory, verbose_name="Документ")
    comment = models.ForeignKey(ElectNewComment, related_name='elect_new_comment_doc', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = "Документ коммента к новости депутата"
        verbose_name_plural = "Документы коммента к новости депутата"

class ElectNewCommentPhoto(models.Model):
    file = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to=upload_to_user_directory, processors=[Transpose(), ResizeToFit(width=1024, upscale=False)])
    comment = models.ForeignKey(ElectNewComment, related_name='elect_new_comment_photo', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Фото коммента к новости депутата'
        verbose_name_plural = 'Фото коммента к новости депутата'
