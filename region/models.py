from django.db import models
from django.db.models import Q
from autoslug import AutoSlugField
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField


class Region(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название региона")
	slug = AutoSlugField(populate_from='name', unique=True)
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	svg = models.CharField(max_length=1000, blank=True, verbose_name="SVG")
	image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 90}, upload_to="regions/%Y/%m/%d/", processors=[ResizeToFit(width=1600, upscale=False)], verbose_name="Главное изображение")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["name"]
		verbose_name = "Регион"
		verbose_name_plural = "Регионы"

	def get_all_elects(self):
		from elect.models import Elect

		query = Q(Q(region=self) | Q(region__slug="all_regions"))
		return Elect.objects.filter(query)

	def is_have_elects(self):
		from elect.models import Elect

		query = Q(Q(region=self) | Q(region__slug="all_regions"))
		return Elect.objects.filter(query).exists()

	def get_cities(self):
		return self.cities_region.filter(region=self)
