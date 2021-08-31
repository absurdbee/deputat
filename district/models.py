from django.db import models
from django.db.models import Q
from autoslug import AutoSlugField
from region.models import Region


class District(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название")
	slug = AutoSlugField(populate_from='name', unique=True, db_index=True)
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts_region", blank=True, null=True, verbose_name="Регион")

	point = models.PositiveIntegerField(default=0, verbose_name="Общее количество кармы")
	total_costs = models.PositiveIntegerField(default=0, verbose_name="Общие доходы граждан")
	total_revenue = models.PositiveIntegerField(default=0, verbose_name="Общие расходы граждан")

	total_voters = models.CharField(max_length=50, verbose_name="Всего избирателей")
	total_place = models.CharField(max_length=50, verbose_name="Всего мест")
	total_candidate = models.CharField(max_length=50, verbose_name="Всего кандидатов")
	man_procent = models.CharField(max_length=50, verbose_name="Процент мужчин")

	total_er = models.CharField(max_length=50, verbose_name="Всего из Единой России")
	total_kprf = models.CharField(max_length=50, verbose_name="Всего из КПРФ")
	total_ldpr = models.CharField(max_length=50, verbose_name="Всего из ЛДПР")
	total_sr = models.CharField(max_length=50, verbose_name="Всего из Справедливой России")
	total_self = models.CharField(max_length=50, verbose_name="Всего самовыдвиженцев")

	link = models.CharField(max_length=50, verbose_name="Ссылка для парсинга")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Район"
		verbose_name_plural = "Район"

	def __str__(self):
		return self.name

		
