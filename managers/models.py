from django.db import models
from django.conf import settings


class UserStaff(models.Model):
    ADMINISTRATOR, MODERATOR, EDITOR, ADVERTISER = 'A', 'M', 'E', 'R'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в профиле'
        verbose_name_plural = 'Полномочия в профиле'

class CommunityStaff(models.Model):
    ADMINISTRATOR, MODERATOR, EDITOR, ADVERTISER = 'A', 'M', 'E', 'R'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_community_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в сообществе'
        verbose_name_plural = 'Полномочия в сообществе'

class ElectNewUserStaff(models.Model):
    ADMINISTRATOR, MODERATOR, EDITOR, ADVERTISER = 'A', 'M', 'E', 'R'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='elect_new_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в активностях депутатов'
        verbose_name_plural = 'Полномочия в активностях депутатов'

class SurveyUserStaff(models.Model):
    ADMINISTRATOR, MODERATOR, EDITOR, ADVERTISER = 'A', 'M', 'E', 'R'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в опросах'
        verbose_name_plural = 'Полномочия в опросах'

class DocUserStaff(models.Model):
    ADMINISTRATOR, MODERATOR, EDITOR, ADVERTISER = 'A', 'M', 'E', 'R'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в документах'
        verbose_name_plural = 'Полномочия в документах'

class PhotoUserStaff(models.Model):
    ADMINISTRATOR, MODERATOR, EDITOR, ADVERTISER = 'A', 'M', 'E', 'R'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в фотографиях'
        verbose_name_plural = 'Полномочия в фотографиях'

class VideoUserStaff(models.Model):
    ADMINISTRATOR, MODERATOR, EDITOR, ADVERTISER = 'A', 'M', 'E', 'R'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в видеозаписях'
        verbose_name_plural = 'Полномочия в видеозаписях'

class AudioUserStaff(models.Model):
    ADMINISTRATOR, MODERATOR, EDITOR, ADVERTISER = 'A', 'M', 'E', 'R'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='music_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в аудиозаписях'
        verbose_name_plural = 'Полномочия в аудиозаписях'


class CanWorkStaffUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_user', verbose_name="Создатель персонала")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей")
    can_work_support = models.BooleanField(default=False, verbose_name="Может добавлять техподдержку")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала'
        verbose_name_plural = 'Создатели персонала'

class CanWorkStaffCommunity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_community', verbose_name="Создатель персонала")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей")
    can_work_support = models.BooleanField(default=False, verbose_name="Может добавлять техподдержку")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала сообщетсв'
        verbose_name_plural = 'Создатели персонала сообщетсв'

class CanWorkStaffElectNewUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_elect_new_user', verbose_name="Создатель персонала в записях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов активностей депутатов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов активностей депутатов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов активностей депутатов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей активностей депутатов")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала активностей депутатов'
        verbose_name_plural = 'Создатели персонала активностей депутатов'

class CanWorkStaffSurveyUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_survey_user', verbose_name="Создатель персонала в записях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов опросов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов опросов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов опросов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей опросов")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала опросов'
        verbose_name_plural = 'Создатели персонала опросов'

class CanWorkStaffDocUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_doc_user', verbose_name="Создатель персонала в товарах")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов докуметов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов докуметов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов докуметов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей докуметов")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала докуметов'
        verbose_name_plural = 'Создатели персонала докуметов'

class CanWorkStaffPhotoUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_photo_user', verbose_name="Создатель персонала в фотографиях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов фотографий")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов фотографий")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов фотографий")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей фотографий")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала фотографий'
        verbose_name_plural = 'Создатели персонала фотографий'

class CanWorkStaffVideoUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_video_user', verbose_name="Создатель персонала в видеозаписях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов видеозаписей")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов видеозаписей")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов видеозаписей")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей видеозаписей")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала видеозаписей'
        verbose_name_plural = 'Создатели персонала видеозаписей'

class CanWorkStaffAudioUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_audio_user', verbose_name="Создатель персонала в аудиозаписях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов аудиозаписей")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов аудиозаписей")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов аудиозаписей")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей аудиозаписей")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала аудиозаписей'
        verbose_name_plural = 'Создатели персонала аудиозаписей'


class ModerationCategory(models.Model):
    SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_MEDIUM, SEVERITY_LOW = 'C', 'H', 'M', 'L'
    SEVERITIES = (
        (SEVERITY_CRITICAL, 'Критический'),
        (SEVERITY_HIGH, 'Высокий'),
        (SEVERITY_MEDIUM, 'Средний'),
        (SEVERITY_LOW, 'Низкий'),
    )
    name = models.CharField(max_length=32, blank=False, null=False, verbose_name="Название")
    title = models.CharField(max_length=64, blank=False, null=False, verbose_name="Заголовок")
    description = models.CharField(max_length=255, blank=False, null=False, verbose_name="Описание")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    severity = models.CharField(max_length=5, choices=SEVERITIES,verbose_name="Строгость")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория модерации'
        verbose_name_plural = 'Категории модерации'


USER, COMMUNITY = 'USE', 'COM'
ELECT_NEW, ELECT_NEW_COMMENT = 'ELE', 'ELEC'
PHOTO_LIST, PHOTO, PHOTO_COMMENT = 'PHL', 'PHO', 'PHOC'
DOC_LIST, DOC = 'DOL', 'DOC'
MUSIC_LIST, MUSIC = 'MUL', 'MUS'
SURVEY_LIST, SURVEY = 'SUL', 'SUR'
VIDEO_LIST, VIDEO, VIDEO_COMMENT = 'VIL', 'VID', 'VIDC'
TYPE = (
    (USER, 'Пользователь'), (COMMUNITY, 'Сообщество'),
    (MUSIC_LIST, 'Плейлист'), (MUSIC, 'Трек'),
    (SURVEY_LIST, 'Список опросов'), (SURVEY, 'Опрос'),
    (ELECT_NEW, 'Активность депутата'), (ELECT_NEW_COMMENT, 'Коммент к активности депутата'),
    (DOC_LIST, 'Список документов'), (DOC, 'документ'),
    (PHOTO_LIST, 'Список фотографий'), (PHOTO, 'Фотография'), (PHOTO_COMMENT, 'Коммент к фотографии'),
    (VIDEO_LIST, 'Список роликов'), (VIDEO, 'Ролик'), (VIDEO_COMMENT, 'Коммент к ролику'),
)

class Moderated(models.Model):
    # рассмотрение жалобы на объект, получаемфй по attach. Применение санкций или отвергание жалобы. При применении удаление жалоб-репортов
    PENDING, SUSPEND, CLOSE, BANNER_GET, REJECTED = 'P', 'S', 'C', 'BG', 'R'
    STATUS = (
        (PENDING, 'На рассмотрении'),
        (SUSPEND, 'Объект заморожен'),
        (CLOSE, 'Объект закрыт'),
        (BANNER_GET, 'Объекту присвоен баннер'),
        (REJECTED, 'Отвергнутый'),
    )
    description = models.TextField(max_length=300, blank=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUS, default=PENDING, verbose_name="Статус")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Класс объекта")
    object_id = models.PositiveIntegerField(default=0, verbose_name="id объекта")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Проверяемый объект'
        verbose_name_plural = 'Проверяемые объект'

    @classmethod
    def create_moderated_object(cls, type, object_id):
        return cls.objects.create(type=type, object_id=object_id)

    @classmethod
    def _get_or_create_moderated_object(cls, type, object_id):
        try:
            moderated_object = cls.objects.get(type=type, object_id=object_id)
            moderated_object.verified = False
            moderated_object.save(update_fields=['verified'])
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(type=type, object_id=object_id)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object(cls, type, object_id):
        return cls._get_or_create_moderated_object(type=type, object_id=object_id)

    def reports_count(self):
        # кол-во жалоб на пользователя
        return self.reports.count()

    def reports_count_ru(self):
        count = self.reports_count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " жалоба"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " жалобы"
        else:
            return str(count) + " жалоб"

    def is_verified(self):
        # проверен ли пользователь
        return self.verified
    def is_suspend(self):
        # Объект заморожен
        return self.status == Moderated.SUSPEND
    def is_pending(self):
        # Жалоба рассматривается
        return self.status == Moderated.PENDING
    def is_bloked(self):
        # Объект блокирован
        return self.status == Moderated.BLOCKED
    def is_banner(self):
        # Объект блокирован
        return self.status == Moderated.BANNER_GET

    def create_suspend(self, manager_id, duration_of_penalty):
        self.verified = True

        moderation_expiration = timezone.now() + duration_of_penalty
        ModerationPenalty.create_suspension_penalty(moderated_object=self, manager_id=manager_id, type=self.type, object_id=self.object_id, expiration=moderation_expiration)
        self.save()
    def create_warning_banner(self, manager_id):
        self.verified = True
        self.save()
        ModerationPenaltyUser.create_banner_penalty(moderated_object=self, manager_id=manager_id, type=self.type, object_id=self.object_id)
    def create_close(self, object, description, manager_id):
        self.status = Moderated.CLOSE
        self.description = description
        self.verified = True
        self.save()
        ModerationPenalty.create_close_penalty(moderated_object=self, manager_id=manager_id, type=self.type, object_id=self.object_id)
        if object.community:
            object.close_item(object.community)
        else:
            object.close_item(None)
    def delete_close(self, object, manager_id):
        obj = ModerationPenalty.objects.get(moderated_object=self, type=self.type, object_id=self.object_id)
        obj.delete()
        if object.community:
            object.abort_close_item(object.community)
        else:
            object.close_item(None)
        self.delete()
    def delete_suspend(self, manager_id):
        obj = ModerationPenalty.objects.get(moderated_object=self, type=self.type, object_id=self.object_id)
        obj.delete()
        self.delete()
    def delete_warning_banner(self, manager_id):
        obj = ModerationPenalty.objects.get(moderated_object=self, type=self.type, object_id=self.object_id)
        obj.delete()
        self.delete()

    def unverify_moderation(self, manager_id):
        self.verified = False
        self.moderated_object.all().delete()
        self.save()

    def reject_moderation(self, manager_id):
        self.verified = True
        self.status = ModeratedUser.REJECTED
        self.save()

    def get_reports(self):
        return self.reports.all()

    def get_btn_console(self):
        return '<div class="border-top btn_console"><a class="create_user_suspend pointer">Заморозить</a>| <a class="create_user_close pointer">Заблокировать</a>| <a class="create_user_warning_banner pointer">Повесить баннер</a>| <a class="create_user_rejected pointer">Отклонить</a></div>'

    def get_user(self, user_id):
        try:
            from users.models import User
            user = User.objects.get(pk=user_id)
            reports, count = '', 0
            for report in self.reports.all():
                count += 1
                reports = ''.join([reports, '<p class="mb-1">', str(count), '. ', report.get_type_display(), '</p><p class="mb-2">', report.description, '</p>'])
            return ''.join(['<div class="media"><a href="/users/', str(user_id), '" class="ajax"><figure><img src="', user.get_avatar(), \
            '" style="width: 90px;" alt="image"></figure></a><div class="media-body pl-1"><h6 class="my-0 mt-1"><a href="/users/', \
            str(user_id), '" class="ajax"><h6 class="mt-1">', user.get_full_name(), '</h6></a> ', self.reports_count_ru(), \
            '</h6><div class="">', reports, '</div><div class="border-top btn_console" data-pk', str(user_id), '><a class="create_user_suspend pointer">Заморозить</a> | <a class="create_user_close pointer">Заблокировать</a> | <a class="create_user_warning_banner pointer">Повесить баннер</a> | <a class="create_user_rejected pointer">Отклонить</a></div></div></div>'])
        except:
            return '<div class="media">Ошибка отображения данных</div>'



    @classmethod
    def get_moderation_users(cls):
        return cls.objects.filter(type="USE", verified=False)
    @classmethod
    def get_moderation_communities(cls):
        return cls.objects.filter(type="COM", verified=False)

    @classmethod
    def get_moderation_elect_news(cls):
        return cls.objects.filter(verified=False, type__contains="EL")

    @classmethod
    def get_moderation_photos(cls):
        return cls.objects.filter(verified=False, type__contains="PH")

    @classmethod
    def get_moderation_videos(cls):
        return cls.objects.filter(verified=False, type__contains="VI")

    @classmethod
    def get_moderation_audios(cls):
        return cls.objects.filter(verified=False, type__contains="MU")

    @classmethod
    def get_moderation_survey(cls):
        return cls.objects.filter(verified=False, type__contains="SU")

    @classmethod
    def get_moderation_docs(cls):
        return cls.objects.filter(verified=False, type__contains="DO")


class ModerationReport(models.Model):
    # жалобы на объект.
    PORNO = 'P'
    NO_CHILD = 'NC'
    SPAM = 'S'
    BROKEN = 'B'
    FRAUD = 'F'
    CLON = 'K'
    OLD_PAGE = 'OP'
    DRUGS = 'D'
    NO_MORALITY = 'NM'
    RHETORIC_HATE = "RH"
    UNETHICAL = "U"
    TYPE = (
        (PORNO, 'Порнография'),
        (NO_CHILD, 'Для взрослых'),
        (SPAM, 'Рассылка спама'),
        (BROKEN, 'Оскорбительное поведение'),
        (FRAUD, 'Мошенничество'),
        (CLON, 'Клон моей страницы'),
        (OLD_PAGE, 'Моя старая страница'),
        (DRUGS, 'Наркотики'),
        (NO_MORALITY, 'Не нравственный контент'),
        (RHETORIC_HATE, 'Риторика ненависти'),
        (UNETHICAL, 'Неэтичное поведение'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(Moderated, on_delete=models.CASCADE, related_name='reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, blank=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")

    @classmethod
    def create_moderation_report(cls, reporter_id, _type, object_id, description, type):
        moderated_object = Moderated.get_or_create_moderated_object(type=_type, object_id=object_id)
        return cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на объект'
        verbose_name_plural = 'Жалобы на объект'


class ModerationPenalty(models.Model):
    # сами санкции против объекта.
    SUSPENSION, CLOSE, BANNER = 'S', 'C', 'BA'
    STATUSES = (
        (SUSPENSION, 'Приостановлено'), (CLOSE, 'Закрыто'), (BANNER, 'Вывешен баннер'),
    )

    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_penalties', verbose_name="Менеджер")
    expiration = models.DateTimeField(null=True, blank=True, verbose_name="Окончание")
    moderated_object = models.ForeignKey(Moderated, on_delete=models.CASCADE, related_name='moderated_object', verbose_name="Объект")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Класс объекта")
    object_id = models.PositiveIntegerField(default=0, verbose_name="id объекта")
    status = models.CharField(max_length=5, choices=STATUSES, verbose_name="Тип")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Оштрафованный объект'
        verbose_name_plural = 'Оштрафованные объект'

    @classmethod
    def create_suspension_penalty(cls, object_id, type, manager_id, moderated_object, expiration):
        try:
            obj = cls.objects.get(moderated_object=moderated_object)
            obj.delete()
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.SUSPENSION, expiration=expiration)
        except:
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.SUSPENSION, expiration=expiration)
    @classmethod
    def create_close_penalty(cls, object_id, type, manager_id, moderated_object):
        try:
            obj = cls.objects.get(moderated_object=moderated_object)
            obj.delete()
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.CLOSE)
        except:
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.CLOSE)
    @classmethod
    def create_banner_penalty(cls, object_id, type, manager_id, moderated_object):
        try:
            obj = cls.objects.get(moderated_object=moderated_object)
            obj.delete()
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.BANNER)
        except:
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.BANNER)

    def is_suspend(self):
        # Объект заморожен
        return self.status == 'S'
    def is_closed(self):
        # Объект блокирован
        return self.status == 'C'
    def is_banner(self):
        # Объект блокирован
        return self.status == 'BA'

    @classmethod
    def get_penalty_users(cls, user_id):
        return cls.objects.filter(manager__id=user_id, type="USE")
    @classmethod
    def get_penalty_communities(cls, user_id):
        return cls.objects.filter(manager__id=user_id, type="COM")

    @classmethod
    def get_penalty_elect_news(cls, user_id):
        return cls.objects.filter(manager__id=user_id, type__contains="EL")

    @classmethod
    def get_penalty_photos(cls, user_id):
        return cls.objects.filter(manager__id=user_id, type__contains="PH")

    @classmethod
    def get_penalty_videos(cls, user_id):
        return cls.objects.filter(manager__id=user_id, type__contains="VI")

    @classmethod
    def get_penalty_audios(cls, user_id):
        return cls.objects.filter(manager__id=user_id, type__contains="MU")

    @classmethod
    def get_penalty_surveys(cls, user_id):
        return cls.objects.filter(manager__id=user_id, type__contains="SU")

    @classmethod
    def get_penalty_docs(cls, user_id):
        return cls.objects.filter(manager__id=user_id, type__contains="DO")

    def get_user(self, user_id):
        #try:
        from users.models import User
        user = User.objects.get(pk=user_id)
        if self.is_suspend():
            span = '<span class="small">До ', str(self.expiration), '</span>(<a class="small remove_user_suspend pointer">Отменить заморозку</a> |<a class="small user_unverify pointer">Отменить проверку</a>)'
        elif self.is_closed():
            span = '<span class="small">Заблокирован</span>(<a class="small remove_user_bloсk pointer">Отменить блокировку</a> |<a class="small user_unverify pointer">Отменить проверку</a>)'
        elif self.is_banner():
            span = '<span class="small">Баннер предупреждения</span>(<a class="small remove_user_warning_banner pointer">Убрать баннер</a> |<a class="small user_unverify pointer">Отменить проверку</a>)'
        else:
            span = '<span class="small">Санкции не применены</span>'
        return ''.join(['<div class="media"><a href="/users/', str(user_id), '" class="ajax"><figure><img src="', user.get_avatar(), \
        '" style="width: 90px;" alt="image"></figure></a><div class="media-body pl-1"><h6 class="my-0 mt-1"><a href="/users/', \
        str(user_id), '" class="ajax"><h6 class="mt-1">', user.get_full_name(), \
        '</h6></a></h6><div class=""></div><div class="border-top btn_console" data-pk', str(user_id), '>', span, '</div></div></div>'])
        #except:
        #    return '<div class="media">Ошибка отображения данных</div>'
