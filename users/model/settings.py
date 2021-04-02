from django.conf import settings
from django.db import models


class UserNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notify', verbose_name="Пользователь")
    comment = models.BooleanField(default=True, verbose_name="Комментарии на мои активности")
    reaction = models.BooleanField(default=True, verbose_name="Реакции на мои активности")
    comment_reaction = models.BooleanField(default=True, verbose_name="Реакции на мои комментарии")
    reply = models.BooleanField(default=True, verbose_name="Ответы на мои активности")
    admin = models.BooleanField(default=True, verbose_name="Административные уведомления")

    def __str__(self):
        return self.user.last_name

    class Meta:
        verbose_name = 'Настройка уведомдений пользователя'
        verbose_name_plural = 'Настройки уведомдений пользователя'
        index_together = [('id', 'user'),]


class UserPrivate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_private', verbose_name="Пользователь")
    city = models.BooleanField(default=False, verbose_name="Город виден всем")
    networks = models.BooleanField(default=True, verbose_name="Соцсети открыты")
    old = models.BooleanField(default=True, verbose_name="Возраст открыт")
    subscribers = models.BooleanField(default=True, verbose_name="Подписки открыты")
    other = models.BooleanField(default=True, verbose_name="Образование/сфера занятости открыты")

    def __str__(self):
        return self.user.last_name

    class Meta:
        verbose_name = 'Настройка приватности пользователя'
        verbose_name_plural = 'Настройки приватности пользователя'
        index_together = [('id', 'user'),]
