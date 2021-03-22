from django.db import models
from django.db.models import Q
from autoslug import AutoSlugField


class City(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название")
	slug = AutoSlugField(populate_from='name', unique=True, db_index=True)
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="+", blank=True, null=True, verbose_name="Регион")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Город"
		verbose_name_plural = "Города"

	def __str__(self):
		return self.name
