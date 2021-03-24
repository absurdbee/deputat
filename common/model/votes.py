from django.db import models
from django.conf import settings
from blog.models import Blog, ElectNew
from common.model.comments import ElectNewComment, BlogComment


"""
    Группируем все таблицы реакций здесь:
    1. Реакции на статьи блога проекта,
    2. Реакции на новостей чиновника,
    3. Реакции на комменты к новостям чиновника,
    4. Реакции на статьи блога
"""

class BlogVotes(models.Model):
    LIKE = "LIK"
    DISLIKE = "DIS"
    INERT = "INE"
    VOTES = ((DISLIKE, 'Не оценил'),(LIKE, 'Оценил'),(INERT, 'Объект инертный'))

    vote = models.CharField(default=0, max_length=5, verbose_name="Голос", choices=VOTES) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

class ElectNewVotes2(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = ((DISLIKE, 'Не нравится'),(LIKE, 'Нравится'))

    vote = models.IntegerField(default=0, verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    new = models.ForeignKey(ElectNew, on_delete=models.CASCADE)


class ElectNewCommentVotes(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = ((DISLIKE, 'Не нравится'),(LIKE, 'Нравится'))

    vote = models.IntegerField(default=0, verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    comment = models.ForeignKey(ElectNewComment, on_delete=models.CASCADE)

class BlogCommentVotes(models.Model):
    from common.model.comments import BlogComment
    LIKE = 1
    DISLIKE = -1
    VOTES = ((DISLIKE, 'Не нравится'),(LIKE, 'Нравится'))

    vote = models.IntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE)
