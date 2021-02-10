from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from blog.models import ElectNew, ElectVotes
from elect.models import Elect, SubscribeElect
from common.utils import try_except
from users.helpers import upload_to_user_directory


"""
    Группируем все таблицы пользователя здесь:
    1. Сам пользователь
"""
class User(AbstractUser):
    DELETED = 'DE'
    BLOCKED = 'BL'
    PHONE_NO_VERIFIED = 'PV'
    STANDART = 'ST'
    MANAGER = 'MA'
    SUPERMANAGER = 'SM'
    PERM = (
        (DELETED, 'Удален'),
        (BLOCKED, 'Заблокирован'),
        (PHONE_NO_VERIFIED, 'Телефон не подтвержден'),
        (STANDART, 'Обычные права'),
        (MANAGER, 'Менеджер'),
        (SUPERMANAGER, 'Суперменеджер'),
    )

    last_activity = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Активность')
    phone = models.CharField(max_length=17, blank=True, null=True, verbose_name='Телефон')
    perm = models.CharField(max_length=5, choices=PERM, default=PHONE_NO_VERIFIED, verbose_name="Уровень доступа")
    b_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    #USERNAME_FIELD = 'phone'

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
        elect_subscribers = SubscribeElect.objects.filter(user_id=self.pk).values("elect_id")
        elect_ids = [elect['elect_id'] for elect in elect_subscribers]
        return Elect.objects.filter(id__in=elect_ids)

    def get_elect_subscribers_count(self):
        count = SubscribeElect.objects.filter(user_id=self.pk).values("pk").count()
        return count

    def get_like_news(self):
        likes = ElectVotes.objects.filter(user_id=self.pk, vote=ElectVotes.LIKE).values("parent_id")
        news_ids = [new['parent_id'] for new in likes]
        return ElectNew.objects.filter(id__in=news_ids)

    def get_like_news_count(self):
        count = ElectVotes.objects.filter(user_id=self.pk, vote=ElectVotes.LIKE).values("parent_id").count()
        return count

    def get_dislike_news(self):
        dislikes = ElectVotes.objects.filter(user_id=self.pk, vote=ElectVotes.DISLIKE).values("parent_id")
        news_ids = [new['parent_id'] for new in dislikes]
        return ElectNew.objects.filter(id__in=news_ids)

    def get_dislike_news_count(self):
        count = ElectVotes.objects.filter(user_id=self.pk, vote=ElectVotes.DISLIKE).values("parent_id").count()
        return count

    def is_deleted(self):
        return try_except(self.perm == User.DELETED)
    def is_blocked(self):
        return try_except(self.perm == User.BLOCKED)
    def is_manager(self):
        return try_except(self.perm == User.MANAGER)
    def is_supermanager(self):
        return try_except(self.perm == User.SUPERMANAGER)
    def is_no_phone_verified(self):
        return try_except(self.perm == User.PHONE_NO_VERIFIED)

    def create_s_avatar(self, photo_input):
        from easy_thumbnails.files import get_thumbnailer

        self.s_avatar = photo_input
        self.save(update_fields=['s_avatar'])
        new_img = get_thumbnailer(self.s_avatar)['small_avatar'].url.replace('media/', '')
        self.s_avatar = new_img
        return self.save(update_fields=['s_avatar'])

    def create_b_avatar(self, photo_input):
        from easy_thumbnails.files import get_thumbnailer

        self.b_avatar = photo_input
        self.save(update_fields=['b_avatar'])
        new_img = get_thumbnailer(self.b_avatar)['avatar'].url.replace('media/', '')
        self.b_avatar = new_img
        self.save(update_fields=['b_avatar'])
        return self.save(update_fields=['b_avatar'])

    def get_b_avatar(self):
        try:
            return self.b_avatar.url
        except:
            return None

    def get_avatar(self):
        try:
            return self.s_avatar.url
        except:
            return '/static/images/user.png'
