from django.db import models
from django.conf import settings


"""
    Группируем "другие" таблицы здесь:
    1. Телефонные коды, присылаемые пользователям при подтверждении телефона
"""

class PhoneCodes(models.Model):
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    code = models.PositiveSmallIntegerField(default=0, verbose_name="Код")
    id = models.BigAutoField(primary_key=True)
