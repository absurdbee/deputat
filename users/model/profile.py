from django.conf import settings
from django.db import models


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
        return '{} - {}'.format(self.user.get_full_name(), self.ip_1)
