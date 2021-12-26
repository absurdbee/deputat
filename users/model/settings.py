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
    ALL_CAN, FOLLOWS, NO, FOLLOWS_BUT, SOME_FOLLOWS = 1,2,3,4,5
    PERM = (
        (ALL_CAN, 'Все пользователи'),
        (FOLLOWS, 'На кого я подписан'),
        (NO, 'Никто'),
        (FOLLOWS_BUT, 'На кого я подписан, кроме'),
        (SOME_FOLLOWS, 'Некоторые из тех, на кого я подписан'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_private', verbose_name="Пользователь")
    city = models.BooleanField(default=False, verbose_name="Город виден всем")
    networks = models.BooleanField(default=True, verbose_name="Соцсети открыты")
    old = models.BooleanField(default=False, verbose_name="Возраст открыт")
    subscribers = models.BooleanField(default=True, verbose_name="Подписки открыты")
    other = models.BooleanField(default=True, verbose_name="Образование/сфера занятости открыты")
    can_send_message = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто пишет сообщения")
    can_add_in_chat = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто приглашает в беседы")

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

    @classmethod
    def create_key(cls, user, key):
        item = cls.objects.create(user=user, key=key)
        return item

    def __str__(self):
        return self.user.last_name

class DeputatSend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", verbose_name="Пользователь", on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, blank=True, verbose_name="Описание спообов идентификации")

    @classmethod
    def create_item(cls, user, text):
        item = cls.objects.create(user=user, text=text)
        user.type = 'DEPS'
        user.save(update_fields=["type"])
        return item
