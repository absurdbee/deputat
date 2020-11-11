from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from users.helpers import upload_to_user_directory
from blog.models import ElectNew, SubscribeElect, ElectVotes


"""
    Группируем все таблицы пользователя здесь:
    1. Сам пользователь
"""
class User(AbstractUser):
    last_activity = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Активность')
    avatar = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to=upload_to_user_directory, processors=[Transpose(), ResizeToFit(width=500, height=500)], verbose_name="Аватар")

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    def get_joined(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.last_activity)

    def is_online(self):
        from datetime import datetime, timedelta

        now = datetime.now()
        onl = self.last_activity + timedelta(minutes=5)
        if now < onl:
            return True
        else:
            return False

    def get_news(self):
        user_news = ElectNew.objects.filter(creator_id=self.pk)
        return user_news

    def get_news_count(self):
        count = ElectNew.objects.filter(creator_id=self.pk).values("pk").count()
        return count

    def get_elect_subscribers(self):
        elect_subscribers = SubscribeElect.objects.filter(user_id=self.pk)
        return elect_subscribers

    def get_elect_subscribers_count(self):
        count = SubscribeElect.objects.filter(user_id=self.pk).values("pk").count()
        return count

    def get_like_news(self):
        likes = ElectVotes.objects.filter(user_id=self.pk, vote=ElectVotes.LIKE).values("parent_id")
        news_ids = [new['parent_id'] for new in likes]
        return ElectNew.objects.filter(id__in=news_ids)

    def get_like_news_count(self):
        count = ElectVotes.objects.filter(user_id=self.pk, vote=ElectVotes.LIKE).values("parent_id")
        return count

    def get_dislike_news(self):
        dislikes = ElectVotes.objects.filter(user_id=self.pk, vote=ElectVotes.DISLIKE).values("parent_id")
        news_ids = [new['parent_id'] for new in dislikes]
        return ElectNew.objects.filter(id__in=news_ids)

    def get_dislike_news_count(self):
        count = ElectVotes.objects.filter(user_id=self.pk, vote=ElectVotes.DISLIKE).values("parent_id")
        return count
