from django.db import models
from django.db.models import Q
from autoslug import AutoSlugField
from region.models import Region


class City(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название")
	slug = AutoSlugField(populate_from='name', unique=True, db_index=True)
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities_region", blank=True, null=True, verbose_name="Регион")
	point = models.PositiveIntegerField(default=0, verbose_name="Общее количество кармы")
	total_costs = models.PositiveIntegerField(default=0, verbose_name="Общие доходы граждан")
    total_revenue = models.PositiveIntegerField(default=0, verbose_name="Общие расходы граждан")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Город"
		verbose_name_plural = "Города"

	def __str__(self):
		return self.name
