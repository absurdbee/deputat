from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q


class Elect(models.Model):
    name = models.CharField(max_length=255, verbose_name="ФИО")
    image = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to="elect/%Y/%m/%d/", processors=[Transpose(), ResizeToFit(width=500, upscale=False)], verbose_name="Аватар")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    list = models.ManyToManyField('lists.ElectList', blank=True, related_name='list', verbose_name="Орган гос. власти")
    region = models.ForeignKey('lists.REgion', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Регион, за которым закреплен депутат")

    class Meta:
        verbose_name = "Чиновник"
        verbose_name_plural = "Чиновники"

    def __str__(self):
        return self.title

    def get_elects(self):
        elects = Elect.objects.filter(list=self.list)
        return elects


class LinkElect(models.Model):
    title = models.CharField(max_length=255, verbose_name="Текст ссылки")
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE, blank=True, verbose_name="Чиновник")
    link = models.URLField(max_length=255, verbose_name="Ссылки")

    class Meta:
        verbose_name = "Ссылка для чиновника"
        verbose_name_plural = "Ссылки"

    def __str__(self):
        return self.title
