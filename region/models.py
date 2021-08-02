from django.db import models
from django.db.models import Q
from autoslug import AutoSlugField
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField


class Region(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название региона")
	slug = AutoSlugField(populate_from='name', unique=True)
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	svg = models.TextField(blank=True, verbose_name="SVG")
	image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 90}, upload_to="regions/%Y/%m/%d/", processors=[ResizeToFit(width=1600, upscale=False)], verbose_name="Главное изображение")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["name"]
		verbose_name = "Регион"
		verbose_name_plural = "Регионы"

	def get_elects(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self)
	def get_elects_ids(self):
		from elect.models import Elect
		elects = Elect.objects.filter(region=self).values("id")
		return [i['id'] for i in elects]

	def get_news(self):
		from blog.models import ElectNew
		return ElectNew.objects.filter(elect__in=self.get_elects())

	def get_news_ids(self):
		from blog.models import ElectNew
		ids = ElectNew.objects.filter(elect__in=self.get_elects()).values("id")
		return [i['id'] for i in ids]

	def is_have_elects(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self).exists()

	def get_cities(self):
		return self.cities_region.filter(region=self)
