from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            UserNotifications.objects.create(user=instance)


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

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            UserPrivate.objects.create(user=instance)

class UserSecretKey(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', verbose_name="Пользователь")
    key = models.CharField(max_length=40, blank=True, verbose_name="Ключ доступа")

class DeputatSend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", verbose_name="Пользователь", on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, blank=True, verbose_name="Описание спообов идентификации")

    def create_item(cls, user, text):
        item = cls.objects.create(user=user, text=text)
        return item
