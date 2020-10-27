from django.db import models
from django.db.models import Q


"""
	Группируем все таблицы списков здесь:
	1. Списки депутатов,
	2. категории новостей о депутатах
	3. Категории блога
	4. Регионы России (для закрепления за ними депутатов)
	5. Фракции (для депутатов гос. думы)
"""


class AuthorityList(models.Model):
	name = models.CharField(max_length=100, verbose_name="Список депутатов")
	slug = models.CharField(max_length=100, verbose_name="Англ. название для списка")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	is_reginal = models.BooleanField(default=True, verbose_name="Региональный список")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Список депутатов"
		verbose_name_plural = "Списки депутатов"

	def __str__(self):
		return self.name

	def is_list_not_empty(self):
		return AuthorityList.objects.filter(category_id=self.pk).exists()

	def get_elects(self):
		query = Q(list_id=self.pk)
		list = AuthorityList.objects.filter(query)
		return list

	def get_elects_10(self):
		query = Q(list_id=self.pk)
		list = AuthorityList.objects.filter(query)[:10]
		return list


class ElectNewsCategory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название категории новостей о депутате")
	slug = models.CharField(max_length=100, verbose_name="Англ. название для категории")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

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


class Region(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название региона")
	slug = models.CharField(blank=True, max_length=100, verbose_name="Для ссылки английское название")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	svg = models.CharField(max_length=1000, blank=True, verbose_name="SVG")

	def __str__(self):
		return self.name


	class Meta:
		ordering = ["name"]
		verbose_name = "Регион"
		verbose_name_plural = "Регионы"

	def __str__(self):
		return self.name

	def get_all_elects(self):
		from elect.models import Elect
		query = Q(Q(region=self) | Q(region__slug="all_regions"))
		return Elect.objects.filter(query) 


class Fraction(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название фракции")
	slug = models.CharField(blank=True, max_length=100, verbose_name="Для ссылки английское название")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

	def __str__(self):
		return self.name


	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Фракция"
		verbose_name_plural = "Фракции"

	def __str__(self):
		return self.name
