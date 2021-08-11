from django.db import models


class Organization(models.Model):
	AUTO_BIZNES,ADMIN_STAFF,BANK,SAFETY,ACCOUNTING,SENIOR_MANAGMENT,PUBLIC_SERVICE,EXTRACTION,HOME_STAFF,PURCHASES,INSTALLATION,INET_TELECOM,ART_MASS_MEDIA,CONSULTING,MARKETING,MEDICINE,SCIENCE,STUDENTS,SALES,PRODUCTIONS,WORKING_STAFF,SPORT,INSURANCE,CONSTRUCTIONS,TRANSPORT,TOURISM,MANAGERS,LAWYERS = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19.,20,21,22,23,24,25,26,27,28
	TYPE = (
        	(AUTO_BIZNES, 'Автомобильный бизнес'),
			(ADMIN_STAFF, 'Административный персонал'),
			(BANK, 'Банки, инвестиции, лизинг'),
			(SAFETY, 'Безопасность'),
			(ACCOUNTING, 'Бухгалтерия, управленческий учет, финансы предприятия'),
			(SENIOR_MANAGMENT, 'Высший менеджмент'),
			(PUBLIC_SERVICE, 'Государственная служба, некоммерческие организации'),
			(EXTRACTION, 'Добыча сырья'),
			(HOME_STAFF, 'Домашний персонал'),
			(PURCHASES, 'Закупки'),
			(INSTALLATION, 'Инсталляция и сервис'),
			(INET_TELECOM, 'Информационные технологии, интернет, телеком'),
			(ART_MASS_MEDIA, 'Искусство, развлечения, масс-медиа'),
			(CONSULTING, 'Консультирование'),
			(MARKETING, 'Маркетинг, реклама, PR'),
			(MEDICINE, 'Медицина, фармацевтика'),
			(SCIENCE, 'Наука, образование'),
			(STUDENTS, 'Начало карьеры, студенты'),
			(SALES, 'Продажи'),
			(PRODUCTIONS, 'Производство, сельское хозяйство'),
			(WORKING_STAFF, 'Рабочий персонал'),
			(SPORT, 'Спортивные клубы, фитнес, салоны красоты'),
			(INSURANCE, 'Страхование'),
			(CONSTRUCTIONS, 'Строительство, недвижимость'),
			(TRANSPORT, 'Транспорт, логистика'),
			(TOURISM, 'Туризм, гостиницы, рестораны'),
			(MANAGERS, 'Управление персоналом, тренинги'),
			(LAWYERS, 'Юристы'),
		)
	name = models.CharField(max_length=100, verbose_name="Название")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	image = models.ImageField(blank=True, upload_to="organizations/")
	city = models.ManyToManyField("city.City", related_name='+', verbose_name="Город")
	email_1 = models.EmailField(blank=True, verbose_name="Почта 1")
	email_2 = models.EmailField(blank=True, verbose_name="Почта 2")
	phone_1 = models.CharField(blank=True, max_length=17, verbose_name='Телефон 1')
	phone_2 = models.CharField(blank=True, max_length=17, verbose_name='Телефон 2')
	address_1 = models.CharField(blank=True, max_length=100, verbose_name='Адрес 1')
	address_2 = models.CharField(blank=True, max_length=100, verbose_name='Адрес 2')
	type = models.PositiveSmallIntegerField(choices=TYPE, default=1, verbose_name="Тип деятельности")
	description = models.TextField(max_length=500, blank=True, null=True, verbose_name="Описание")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Организация"
		verbose_name_plural = "Организации"

	def __str__(self):
		return self.name
