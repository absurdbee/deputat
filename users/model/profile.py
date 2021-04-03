from django.db import models
from django.conf import settings
from common.model.comments import BlogComment, ElectNewComment
from blog.models import Blog, ElectNew
from django.contrib.postgres.indexes import BrinIndex


class UserLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_location", verbose_name="Пользователь", on_delete=models.CASCADE)
    city_ru = models.CharField(max_length=100, blank=True, verbose_name="Город по-русски")
    city_en = models.CharField(max_length=100, blank=True, verbose_name="Город по-английски")
    city_lat = models.FloatField(blank=True, null=True, verbose_name="Ширина города")
    city_lon = models.FloatField(blank=True, null=True, verbose_name="Долгота города")
    region_ru = models.CharField(max_length=100, blank=True, verbose_name="Регион по-русски")
    region_en = models.CharField(max_length=100, blank=True, verbose_name="Регион по-английски")
    country_ru = models.CharField(max_length=100, blank=True, verbose_name="Страна по-русски")
    country_en = models.CharField(max_length=100, blank=True, verbose_name="Страна по-английски")
    phone = models.CharField(max_length=5, blank=True, verbose_name="Начало номера")

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"
        index_together = [('id', 'user'),]

    def __str__(self):
        return '{}, {}, {}'.format(self.country_ru, self.region_ru, self.city_ru)

    def get_sity(self):
        return self.city_ru


class IPUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_ip", verbose_name="Пользователь", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(protocol='both', null=True, blank=True, verbose_name="ip 1")

    class Meta:
        verbose_name = "ip пользователя"
        verbose_name_plural = "ip пользователей"
        index_together = [('id', 'user'),]

    def __str__(self):
        return '{} - {}'.format(self.user.get_full_name(), self.ip)


class Bookmarks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_bookmarks", verbose_name="Избранное", on_delete=models.CASCADE)
    blog = models.ManyToManyField(Blog, blank=True, related_name='blog_bookmarks')
    new = models.ManyToManyField(ElectNew, blank=True, related_name='new_bookmarks')
    blog_comment = models.ManyToManyField(BlogComment, blank=True, related_name='blog_comment_bookmarks')
    new_comment = models.ManyToManyField(ElectNewComment, blank=True, related_name='new_comment_bookmarks')

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return self.user.get_full_name()


class UserInfo(models.Model):
    NO_VALUE = "NOV"
    EDUCATION_HIGH = 'EDH'
    EDUCATION_MEDIUM = 'EDM'
    EDUCATION_LOW = 'EDL'

    EDUCATION = 'EDU'
    MEDICAL = 'MED'
    IT = 'IT'

    EDUCATIONS = (
        (NO_VALUE, 'Не выбрано'),
        (EDUCATION_HIGH, 'Высшее образование'),
        (EDUCATION_MEDIUM, 'Среднее специальное'),
        (EDUCATION_LOW, 'Среднее'),
    )
    EMPLOYMENT = (
        (NO_VALUE, 'Не выбрано'),
        (EDUCATION, 'Образование'),
        (MEDICAL, 'Медицина'),
        (IT, 'IT'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_info', verbose_name="Пользователь")
    education = models.CharField(max_length=5, choices=EDUCATIONS, default=NO_VALUE, verbose_name="Образование")
    employment = models.CharField(max_length=5, choices=EMPLOYMENT, default=NO_VALUE, verbose_name="Сфера занятости")
    birthday = models.DateField(blank=True, null=True, verbose_name='День рождения')

    class Meta:
        verbose_name = "Информация о пользователе"
        verbose_name_plural = "Информация о пользователях"

    def __str__(self):
        return self.user.get_full_name()

class UserCheck(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_check', verbose_name="Пользователь")
    email = models.BooleanField(default=False, verbose_name="Почта указана")
    profile_info = models.BooleanField(default=False, verbose_name="О себе заполнено")
    elect_new = models.BooleanField(default=False, verbose_name="Активность написана")
    comment = models.BooleanField(default=False, verbose_name="Комментарий написан")
    reaction = models.BooleanField(default=False, verbose_name="Реакция совершена")
    quard = models.BooleanField(default=False, verbose_name="Плохой контент найден")

    class Meta:
        verbose_name = "Проверка действий пользователя"
        verbose_name_plural = "Проверки действий пользователей"

    def __str__(self):
        return self.user.get_full_name()


class UserTransaction(models.Model):
    NO_REASON = "NOR"
    PAYMENT = 'PAY'
    ADDING = 'ADD'
    AUTOPAYMENT = 'AUP'
    PENALTY = 'PEN'
    REASON_CHOICES = (
        (NO_REASON, 'Не указано'),
        (PAYMENT, 'Оплата'),
        (ADDING, 'Пополнение'),
        (AUTOPAYMENT, 'Автоплатёж'),
        (PENALTY, 'Штраф'), 
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    reason = models.CharField(max_length=5, choices=REASON_CHOICES, default=NO_REASON, verbose_name="Причина изменения счета")
    value = models.PositiveIntegerField(default=0, verbose_name="Сумма транзакции")
    total = models.PositiveIntegerField(default=0, verbose_name="Остаток")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-created"]

    def __str__(self):
        return self.user.get_full_name()

    def get_pretty_value(self):
        if self.reason == UserTransaction.PAYMENT or self.reason == UserTransaction.AUTOPAYMENT:
            return '<span class="font-weight-bolder text-danger">- ' + str(self.value) + '</span>'
        elif self.reason == UserTransaction.ADDING:
            return '<span class="font-weight-bolder text-success">+ ' + str(self.value) + '</span>'
        elif self.reason == UserTransaction.PENALTY:
            return '<span class="font-weight-bolder text-danger">- ' + str(self.value) + '</span>'
