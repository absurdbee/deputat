from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex


class ElectNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто заходит")
    elect = models.PositiveIntegerField(default=0, verbose_name="К какому чиновнику заходит")
    platform = models.PositiveIntegerField(default=0, verbose_name="0 Комп, 1 Телефон")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Просмотр чиновника"
        verbose_name_plural = "Просмотры чиновников"


class ElectNewNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто заходит")
    new = models.PositiveIntegerField(default=0, verbose_name="Какую новость депутата смотрит")
    platform = models.PositiveIntegerField(default=0, verbose_name="0 Комп, 1 Телефон")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Просмотр новости чиновника"
        verbose_name_plural = "Просмотры новостей чиновника"


class BlogNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто смотрит")
    new = models.PositiveIntegerField(default=0, verbose_name="Какую новость проекта смотрит")
    platform = models.PositiveIntegerField(default=0, verbose_name="0 Комп, 1 Телефон")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Просмотр новости проекта"
        verbose_name_plural = "Просмотры новостей проекта"
