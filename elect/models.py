from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q


class Elect(models.Model):
    FRACTION_NULL = 'FN'
    FRACTION_EDINAYA_RUSSIYA = 'FER'
    FRACTION_SPRAVEDLIVAYA_RUSSIYA = 'FSR'
    FRACTION_KPRF = 'FK'
    FRACTION_LDPR = 'FL'
    NON_FRACTION = 'NF'
    FRACTION = (
        (FRACTION_NULL, 'Не депутат, не имеет фракции'),
        (FRACTION_EDINAYA_RUSSIYA, 'Единая Россия'),
        (FRACTION_SPRAVEDLIVAYA_RUSSIYA, 'Справедливая Россия'),
        (FRACTION_KPRF, 'КПРФ'),
        (FRACTION_LDPR, 'ЛДПР'),
        (NON_FRACTION, 'Депутат не входит во фракции'),
    )

    name = models.CharField(max_length=255, verbose_name="ФИО")
    image = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to="elect/%Y/%m/%d/", processors=[Transpose(), ResizeToFit(width=500, upscale=False)], verbose_name="Аватар")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    list = models.ManyToManyField('lists.ElectList', blank=True, related_name='elect_list', verbose_name="Орган гос. власти")
    region = models.ManyToManyField('lists.REgion', blank=True, related_name='elect_region', verbose_name="Регион, за которым закреплен депутат")
    fraction = models.CharField(blank=False, null=False, choices=FRACTION, default=FRACTION_NULL, max_length=4, verbose_name="Фракция депутата")
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    authorization = models.DateField(blank=True, null=True, verbose_name='Дата наделения полномочиями')
    term_of_office = models.DateField(blank=True, null=True, verbose_name='Срок окончания полномочий')
    education = models.ForeignKey(EducationElect, on_delete=models.CASCADE, blank=True, verbose_name="Образование")
    link = models.ForeignKey(LinkElect, on_delete=models.CASCADE, blank=True, verbose_name="Ссылка универсальная")
    election_information = models.CharField(max_length=100, blank=True, verbose_name="Сведения об избрании")


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


class EducationElect(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE, blank=True, verbose_name="Чиновник")
    year = models.PositiveSmallIntegerField(default=0, verbose_name="Год")

    class Meta:
        verbose_name = "Ссылка для чиновника"
        verbose_name_plural = "Ссылки"

    def __str__(self):
        return self.title
