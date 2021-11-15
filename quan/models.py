from django.db import models
from django.conf import settings
from quan.helpers import validate_file_extension
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone


class QuestionsCategory(models.Model):
	name_ru = models.CharField(max_length=100, unique=True, verbose_name="Русское название")
	name_en = models.CharField(max_length=100, unique=True, verbose_name="Английское название")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

	def __str__(self):
		return self.name_ru

	class Meta:
		verbose_name = "Категория вопросов"
		verbose_name_plural = "Категории вопросов"
		ordering = ['order']


class Question(models.Model):
	quest = models.CharField(max_length=100, unique=True, verbose_name="Вопрос")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	category = models.ManyToManyField(QuestionsCategory, related_name='questions_categories', verbose_name="Категории вопроса")

	def __str__(self):
		return str(self.order)

	class Meta:
		verbose_name = "Вопрос"
		verbose_name_plural = "Вопросы"
		ordering = ['order']


class QuestionVote(models.Model):
	DONT_LIKE_THIS = 'DL'
	ANSVER_UNCLEAR = 'AU'
	HAVE_QUESTIONS = 'HQ'
	PROBLEM_SOLVED = 'PS'
	VOIS_TYPES = (
		(DONT_LIKE_THIS, 'Мне не нравится, как всё устроено'),
		(ANSVER_UNCLEAR, 'Ответ неясный'),
		(HAVE_QUESTIONS, 'У меня остались вопросы'),
		(PROBLEM_SOLVED, 'Вопрос решен'),
	)
	type = models.CharField(choices=VOIS_TYPES, max_length=2)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='quest_vois', verbose_name="Впрос")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quest_creator', on_delete=models.CASCADE, verbose_name="Создатель")

	def __str__(self):
		return self.type

	class Meta:
		verbose_name = "Голос"
		verbose_name_plural = "Голоса"


class Support(models.Model):
	QUESTIONS = 'QU'
	COOPERATION = 'CO'
	TECHNICAL_PROBLEMS = 'TP'
	PROJECT_ASSISTANCE = 'PA'
	COPYRIGHT_HOLDERS = 'CH'
	CATEGORY = (
		(COPYRIGHT_HOLDERS, 'Для правообладателей'),
		(TECHNICAL_PROBLEMS, 'Обращение в техподдержку'),
		(QUESTIONS, 'Вопрос / предложение'),
		(COOPERATION, 'Сотрудничество'),
		(PROJECT_ASSISTANCE, 'Помощь проекту'),
	)
	type = models.CharField(choices=CATEGORY, default=QUESTIONS, max_length=2, verbose_name="Тема")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='support_creator', on_delete=models.CASCADE, verbose_name="Пользователь")
	description = models.TextField(max_length=3000, blank=True, verbose_name="Описание")
	created = models.DateTimeField(default=timezone.now, verbose_name="Создано")
	is_read = models.BooleanField(default=False, verbose_name="Прочитано")

	def __str__(self):
		return self.creator.get_full_name()

	class Meta:
		verbose_name = "Обращение в тех. поддержку"
		verbose_name_plural = "Обращения в тех. поддержку"
		ordering = ["-created"]
		indexes = (BrinIndex(fields=['created']),)

	def get_files(self):
		return SupportFile.objects.filter(support_id=self.pk)


class SupportFile(models.Model):
	support = models.ForeignKey(Support, on_delete=models.CASCADE, null=True)
	file = models.FileField(upload_to="support/", validators=[validate_file_extension], verbose_name="Файл")
