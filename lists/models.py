from django.db import models
from django.db.models import Q


"""
	Группируем все таблицы списков здесь:
	1. Списки депутатов,
	2. категории новостей о депутатах
	3. Категории блога
"""


class ElectList(models.Model):
	name = models.CharField(max_length=100,verbose_name="Список депутатов")
	slug = models.CharField(max_length=100,verbose_name="Англ. название для списка")
	order = models.PositiveSmallIntegerField(default=0,verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Список депутатов"
		verbose_name_plural = "Списки депутатов"

	def __str__(self):
		return self.name

	def is_list_not_empty(self):
		return ElectList.objects.filter(category_id=self.pk).exists()

	def get_elects(self):
		query = Q(list_id=self.pk)
		list = ElectList.objects.filter(query)
		return list

	def get_elects_10(self):
		query = Q(list_id=self.pk)
		list = ElectList.objects.filter(query)[:10]
		return list


class ElectNewsCategory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название категории новостей о депутате")
	slug = models.CharField(max_length=100, verbose_name="Англ. название для категории")
	order = models.PositiveSmallIntegerField(default=0,verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Список депутатов"
		verbose_name_plural = "Списки депутатов"


class BlogCategory(models.Model):
	name = models.CharField(max_length=100,verbose_name="Название категории блога")
	slug = models.CharField(max_length=100,verbose_name="Англ. название для ссылки")
	order = models.PositiveSmallIntegerField(default=0,verbose_name="Порядковый номер")
	def __str__(self):
		return self.name
	class Meta:
		ordering = ["order", "name"]
		verbose_name = "категория блога"
		verbose_name_plural = "категории блога"

	def __str__(self):
		return self.name

	def is_article_exists(self):
		return self.blog_categories.filter(category=self).values("pk").exists()

	def get_articles_10(self):
		list = self.blog_categories.filter(category=self)[:10]
		return list

	def get_articles(self):
		list = self.blog_categories.filter(category=self)
		return list
