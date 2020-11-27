from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from lists.models import Region
from django.db.models import Q


"""
    Группируем все таблицы чиновников здесь:
    1. Таблица чиновника,
    2. Таблица ссылки чиновника, много ссылок к одному чиновнику
    3. Таблица образования чиновника, много дипломов к одному чиновнику
    3. Таблица подписки пользователя на чиновника
"""
class Elect(models.Model):
    name = models.CharField(max_length=255, verbose_name="ФИО")
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 90}, upload_to="elect/%Y/%m/%d/", processors=[Transpose(), ResizeToFit(width=500, upscale=False)], verbose_name="Аватар")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    list = models.ManyToManyField('lists.AuthorityList', blank=True, related_name='elect_list', verbose_name="Орган гос. власти")
    region = models.ManyToManyField('lists.Region', blank=True, related_name='elect_region', verbose_name="Регион, за которым закреплен депутат")
    birthday = models.CharField(max_length=100, null=True, verbose_name='Дата рождения')
    authorization = models.CharField(max_length=100, null=True, verbose_name='Дата наделения полномочиями')
    term_of_office = models.CharField(max_length=100, null=True, verbose_name='Срок окончания полномочий')
    election_information = models.CharField(max_length=200, blank=True, verbose_name="Сведения об избрании")
    fraction = models.ForeignKey('lists.Fraction', null=True, on_delete=models.SET_NULL, blank=True, verbose_name="Фракции")

    class Meta:
        verbose_name = "Чиновник"
        verbose_name_plural = "Чиновники"

    def __str__(self):
        return self.name

    def get_first_list(self):
        return self.list.all()[0]

    def get_regions(self):
        regions = self.region.all()
        all_regions = Region.objects.get(slug="all_regions")
        if all_regions in regions:
            return [all_regions,]
        else:
            return regions

    def get_news(self):
        return self.elect_news.all()

    def get_remote_image(self, image_url):
        import os
        from django.core.files import File
        from urllib import request

        result = request.urlretrieve(image_url)
        self.image.save(
            os.path.basename(image_url),
            File(open(result[0], 'rb'))
        )
        self.save()

    def visits_count(self):
        from stst.models import ElectNumbers
        return ElectNumbers.objects.filter(elect=self.pk).values('pk').count()


class LinkElect(models.Model):
    title = models.CharField(max_length=255, verbose_name="Текст ссылки")
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE, blank=True, verbose_name="Чиновник")
    link = models.URLField(max_length=255, verbose_name="Ссылки")

    class Meta:
        verbose_name = "Ссылка для чиновника"
        verbose_name_plural = "Ссылки"

    def __str__(self):
        return self.title


class EducationElect(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE, blank=True, verbose_name="Чиновник")
    year = models.CharField(max_length=10, verbose_name="Год")

    class Meta:
        verbose_name = "Образование чиновника"
        verbose_name_plural = "Образование"

    def __str__(self):
        return self.title


class SubscribeElect(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_subscribe', verbose_name="Пользователь")
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE, related_name='elect_subscribe', verbose_name="Чиновник")

    @classmethod
    def create_elect_subscribe(cls, user_id, elect_id):
        return cls.objects.create(user_id=user_id, elect_id=elect_id)

    @classmethod
    def is_elect_subscribe(cls, elect_id, user_id):
        return cls.objects.filter(Q(elect_id=elect_id, user_id=user_id)).exists()

    class Meta:
        unique_together = ('elect', 'user',)
        indexes = [models.Index(fields=['elect', 'user']),]
