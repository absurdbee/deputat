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
	point = models.PositiveIntegerField(default=0, verbose_name="Общее количество кармы")
	total_costs = models.PositiveIntegerField(default=0, verbose_name="Общие доходы граждан")
	total_revenue = models.PositiveIntegerField(default=0, verbose_name="Общие расходы граждан")
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["name"]
		verbose_name = "Регион"
		verbose_name_plural = "Регионы"

	def get_elects(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self)
	def get_list_elects(self, list):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list=list)

	def get_elects_ids(self):
		from elect.models import Elect
		elects = Elect.objects.filter(region=self).values("id")
		return [i['id'] for i in elects]

	def get_senators(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="senat", type='PUB')
	def is_have_senators(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="senat", type='PUB').exists()

	def get_governors(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="governors", type='PUB')
	def is_have_governors(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="governors", type='PUB').exists()

	def get_commissioner_child(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="commissioner_child", type='PUB')
	def is_have_commissioner_child(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="commissioner_child", type='PUB').exists()

	def get_commissioner_human(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="commissioner_human", type='PUB')
	def is_have_commissioner_human(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="commissioner_human", type='PUB').exists()

	def get_head_hinistry_health(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="head_hinistry_health", type='PUB')
	def is_have_head_hinistry_health(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="head_hinistry_health", type='PUB').exists()

	def get_chapter_min_enlightenment(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="chapter_min_enlightenment", type='PUB')
	def is_have_chapter_min_enlightenment(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="chapter_min_enlightenment", type='PUB').exists()

	def get_head_societies_chambers(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="head_societies_chambers", type='PUB')
	def is_have_head_societies_chambers(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="head_societies_chambers", type='PUB').exists()

	def get_legislative_assembly(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="legislative_assembly", type='PUB')
	def is_have_legislative_assembly(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__slug="legislative_assembly", type='PUB').exists()

	def get_gos_duma(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__category__order=1, type='PUB')
	def is_have_gos_duma(self):
		from elect.models import Elect
		return Elect.objects.filter(region=self, list__category__order=1, type='PUB').exists()

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

	def get_districts(self):
		return self.districts_region2.filter(region=self)
	def get_cities(self):
		return self.cities_region.filter(region=self)
