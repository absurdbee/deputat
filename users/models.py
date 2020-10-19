from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField


class User(AbstractUser):
    last_activity = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Активность')
    avatar = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to="users/%Y/%m/%d/", processors=[ResizeToFit(width=500, height=500)], verbose_name="Аватар")

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
