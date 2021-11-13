from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from common.utils import try_except
from users.helpers import upload_to_user_directory
from district.models import District2

"""
    Группируем все таблицы пользователя здесь:
    1. Сам пользователь
"""

class User(AbstractUser):
    PHONE_NO_VERIFIED, STANDART, DEPUTAT, DEPUTAT_SEND, IDENTIFIED_SEND, IDENTIFIED, MANAGER, SUPERMANAGER = '_PV','STA','DEP','DEPS','IDS','IDE','MAN','SUP'
    CLOSED_DEPUTAT,CLOSED_DEPUTAT_SEND, CLOSED_STANDART, CLOSED_IDENTIFIED_SEND, CLOSED_IDENTIFIED, CLOSED_MANAGER = '_CLOD','_CLODS','_CLOS','_CLOIS','_CLOI','_CLOM'
    DELETED_DEPUTAT,DELETED_DEPUTAT_SEND, DELETED_STANDART, DELETED_IDENTIFIED_SEND, DELETED_IDENTIFIED, DELETED_MANAGER = '_DELD','_DELDS','_DELS','_DELIS','_DELI','_DELM'
    SUSPENDED_DEPUTAT,SUSPENDED_DEPUTAT_SEND, SUSPENDED_STANDART, SUSPENDED_IDENTIFIED_SEND, SUSPENDED_IDENTIFIED, SUSPENDED_MANAGER = '_SUSD','_SUSDS','_SUSS','_SUSIS','_SUSI','_SUSM'
    BANNER_DEPUTAT,BANNER_DEPUTAT_SEND, BANNER_STANDART, BANNER_IDENTIFIED_SEND, BANNER_IDENTIFIED, BANNER_MANAGER = '_BAND','_BANDS','_BANS','_BANIS','_BANI','_BANM'
    TYPE = (
        (PHONE_NO_VERIFIED, 'Телефон не подтвержден'),(STANDART, 'Обычные права'),(DEPUTAT, 'Депутат'),(DEPUTAT_SEND, 'Запрос на депутатство'),(IDENTIFIED_SEND, 'Запрос на идентификацию'),(IDENTIFIED, 'Идентифицированный'),(MANAGER, 'Менеджер'),(SUPERMANAGER, 'Суперменеджер'),
        (DELETED_DEPUTAT, 'Удален депутат'),(DELETED_DEPUTAT_SEND, 'Удален подавший на депутатство'),(DELETED_STANDART, 'Удален'),(DELETED_IDENTIFIED_SEND, 'Удален подавший на идентификацию'),(DELETED_IDENTIFIED, 'Удален идентифиированный'),(DELETED_MANAGER, 'Удален менеджер'),
        (CLOSED_DEPUTAT, 'Закрыт депутат'),(CLOSED_DEPUTAT_SEND, 'Закрыт подавший на депутатство'),(CLOSED_STANDART, 'Закрыт'),(CLOSED_IDENTIFIED_SEND, 'Закрыт подавший на идентификацию'),(CLOSED_IDENTIFIED, 'Закрыт идентифиированный'),(CLOSED_MANAGER, 'Закрыт менеджер'),
        (SUSPENDED_DEPUTAT, 'Заморожен депутат'),(SUSPENDED_DEPUTAT_SEND, 'Заморожен подавший на депутатство'),(SUSPENDED_STANDART, 'Заморожен'),(SUSPENDED_IDENTIFIED_SEND, 'Заморожен подавший на идентификацию'),(SUSPENDED_IDENTIFIED, 'Заморожен идентифиированный'),(SUSPENDED_MANAGER, 'Заморожен менеджер'),
        (BANNER_DEPUTAT, 'Баннер депутат'),(BANNER_DEPUTAT_SEND, 'Баннер подавший на депутатство'),(BANNER_STANDART, 'Баннер'),(BANNER_IDENTIFIED_SEND, 'Баннер подавший на идентификацию'),(BANNER_IDENTIFIED, 'Баннер идентифиированный'),(BANNER_MANAGER, 'Баннер менеджер'),
    )
    MALE, FEMALE, DESCTOP, PHONE = 'Man', 'Fem', 'De', 'Ph'
    GENDER = ((MALE, 'Мужской'),(FEMALE, 'Женский'),)
    DEVICE = ((DESCTOP, 'Комп'),(PHONE, 'Телефон'),)

    last_activity = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Активность')
    phone = models.CharField(max_length=17, unique=True, verbose_name='Телефон')
    type = models.CharField(max_length=6, choices=TYPE, default=PHONE_NO_VERIFIED, verbose_name="Уровень доступа")
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    gender = models.CharField(max_length=5, choices=GENDER, blank=True, verbose_name="Пол")
    device = models.CharField(max_length=5, choices=DEVICE, blank=True, verbose_name="Оборудование")
    #point = models.PositiveIntegerField(default=0, verbose_name="Количество кармы")
    #area = models.ForeignKey('district.District2', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Районы, за которым закреплен депутат")
    city = models.ForeignKey('city.City', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Город")
    level = models.PositiveSmallIntegerField(default=1, verbose_name="Уровень")
    birthday = models.DateField(blank=True, null=True, verbose_name='День рождения')
    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.first_name + " " +  self.last_name

    def get_media_lists(self):
        from lists.models import MediaList
        return MediaList.objects.filter(type=MediaList.LIST, owner=None)
    def is_have_media_list(self):
        from lists.models import MediaList
        return MediaList.objects.filter(type=MediaList.LIST, owner_id=self.pk).exists()
    def get_media_list(self):
        from lists.models import MediaList
        return MediaList.objects.filter(type=MediaList.LIST, owner_id=self.pk)[0]
    def get_or_create_media_list(self):
        from lists.models import MediaList
        if MediaList.objects.filter(type=MediaList.LIST, owner_id=self.pk).exists():
            return MediaList.objects.filter(type=MediaList.LIST, owner_id=self.pk)[0]
        else:
            list = MediaList.objects.create(type=MediaList.LIST, creator_id=self.pk, owner_id=self.pk)
            return list

    def get_verb_gender(self, verb):
        if self.is_women():
            return "W" + verb
        else:
            return verb

    def get_publish_or_created_elect_news_count(self):
        from logs.model.manage_elect_new import ElectNewManageLog

        query =  Q(action_type='ICRE')|Q(action_type='IPUB')
        return ElectNewManageLog.objects.filter(query, manager=self.pk).values("pk").count()

    def is_theme_dark(self):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        return profile.theme == 2

    def get_last_location(self):
        from users.model.profile import UserLocation
        return UserLocation.objects.filter(user=self).first()

    def close_item(self):
        if self.type == "DEP":
            self.type = User.CLOSED_DEPUTAT
        elif self.type == "DEPS":
            self.type = User.CLOSED_DEPUTAT_SEND
        elif self.type == "STA":
            self.type = User.CLOSED_STANDART
        elif self.type == "MAN":
            self.type = User.CLOSED_MANAGER
        elif self.type == "IDS":
            self.type = User.CLOSED_IDENTIFIED_SEND
        elif self.type == "IDE":
            self.type = User.CLOSED_IDENTIFIED
        self.save(update_fields=['type'])
    def abort_close_item(self):
        if self.type == "_CLOD":
            self.type = User.DEPUTAT
        elif self.type == "_CLODS":
            self.type = User.DEPUTAT_SEND
        elif self.type == "_CLOS":
            self.type = User.STANDART
        elif self.type == "_CLOM":
            self.type = User.MANAGER
        elif self.type == "_CLOIS":
            self.type = User.IDENTIFIED_SEND
        elif self.type == "_CLOI":
            self.type = User.IDENTIFIED
        self.save(update_fields=['type'])

    def suspend_item(self):
        if self.type == "DEP":
            self.type = User.SUSPENDED_DEPUTAT
        elif self.type == "DEPS":
            self.type = User.SUSPENDED_DEPUTAT_SEND
        elif self.type == "STA":
            self.type = User.SUSPENDED_STANDART
        elif self.type == "MAN":
            self.type = User.SUSPENDED_MANAGER
        elif self.type == "IDS":
            self.type = User.SUSPENDED_IDENTIFIED_SEND
        elif self.type == "IDE":
            self.type = User.SUSPENDED_IDENTIFIED
        self.save(update_fields=['type'])
    def abort_suspend_item(self):
        if self.type == "_SUSD":
            self.type = User.DEPUTAT
        elif self.type == "_SUSDS":
            self.type = User.DEPUTAT
        elif self.type == "_SUSS":
            self.type = User.STANDART
        elif self.type == "_SUSM":
            self.type = User.MANAGER
        elif self.type == "_SUSIS":
            self.type = User.IDENTIFIED_SEND
        elif self.type == "_SUSI":
            self.type = User.IDENTIFIED
        self.save(update_fields=['type'])

    def get_full_name_genitive(self):
        import pymorphy2
        from string import ascii_letters

        try:
            morph = pymorphy2.MorphAnalyzer()
            if all(map(lambda c: c in ascii_letters, self.first_name)):
                first_name = self.first_name
            else:
                name = morph.parse(self.first_name)[0]
                v1 = name.inflect({'gent'})
                first_name = v1.word.title()
            if all(map(lambda c: c in ascii_letters, self.last_name)):
                last_name = self.last_name
            else:
                surname = morph.parse(self.last_name)[0]
                v2 = surname.inflect({'gent'})
                last_name = v2.word.title()
            return first_name + " " + last_name
        except:
            return self.get_full_name()

    def get_photo_list(self):
        from gallery.models import PhotoList
        query =  Q(creator_id=self.pk, community__isnull=True)
        query.add(Q(Q(type="MAI") | Q(type="_CLOM")), Q.AND)
        return PhotoList.objects.get(query)

    def get_doc_list(self):
        from docs.models import DocList
        query =  Q(creator_id=self.pk, community__isnull=True)
        query.add(Q(Q(type="MAI") | Q(type="_CLOM")), Q.AND)
        return DocList.objects.get(query)
    def get_playlist(self):
        from music.models import SoundList
        query =  Q(creator_id=self.pk, community__isnull=True)
        query.add(Q(Q(type="MAI") | Q(type="_CLOM")), Q.AND)
        return SoundList.objects.get(query)
    def get_video_list(self):
        from video.models import VideoList
        query =  Q(creator_id=self.pk, community__isnull=True)
        query.add(Q(Q(type="MAI") | Q(type="_CLOM")), Q.AND)
        return VideoList.objects.get(query)
    def get_survey_list(self):
        from survey.models import SurveyList
        query =  Q(creator_id=self.pk, community__isnull=True)
        query.add(Q(Q(type="MAI") | Q(type="_CLOM")), Q.AND)
        return SurveyList.objects.get(query)

    def is_have_secret_key(self):
        from users.model.settings import UserSecretKey
        try:
            key = UserSecretKey.objects.get(user=self)
            return key != ""
        except:
            return False

    def get_full_name(self):
        if self.is_identified():
            return self.first_name + " " + self.last_name + ' <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-check"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        else:
            return self.first_name + " " + self.last_name

    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_region_slug(self):
        return self.city.region.slug

    def get_joined(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.last_activity)

    def get_location(self):
        from users.model.profile import UserLocation

        if UserLocation.objects.filter(user=self).exists():
            return UserLocation.objects.filter(user=self).first()
        else:
            return False

    def is_online(self):
        from datetime import datetime, timedelta

        now = datetime.now()
        onl = self.last_activity + timedelta(minutes=5)
        return now < onl

    def get_news(self):
        from blog.models import ElectNew
        return ElectNew.objects.filter(creator_id=self.pk, type="PUB", community__isnull=True)
    def get_my_news(self):
        from blog.models import ElectNew
        query = Q((creator_id=self.pk)|Q(community__isnull=True)) & Q(Q(type="PUB")|Q(type="SUG")|Q(type="REJ"))
        query.add(Q(elect_id__in=self.get_elect_subscribers_ids(), type="PUB"), Q.AND)
        return ElectNew.objects.filter(query)

    def get_news_count(self):
        from blog.models import ElectNew
        return ElectNew.objects.filter(creator_id=self.pk, community__isnull=True).values("pk").count()

    def get_elect_subscribers_ids(self):
        from elect.models import SubscribeElect

        elect_subscribers = SubscribeElect.objects.filter(user_id=self.pk).values("elect_id")
        return [elect['elect_id'] for elect in elect_subscribers]

    def get_elect_subscribers(self):
        from elect.models import Elect

        elect_subscribers = SubscribeElect.objects.filter(user_id=self.pk).values("elect_id")
        elect_ids = [elect['elect_id'] for elect in elect_subscribers]
        return Elect.objects.filter(id__in=self.get_elect_subscribers_ids())

    def is_have_elect_subscribers(self):
        from elect.models import Elect, SubscribeElect

        elect_subscribers = SubscribeElect.objects.filter(user_id=self.pk).values("elect_id")
        elect_ids = [elect['elect_id'] for elect in elect_subscribers]
        return Elect.objects.filter(id__in=elect_ids).exists()

    def is_blocked_with_user_with_id(self, user_id):
        from users.model.profile import UserBlock
        return UserBlock.users_are_blocked(user_a_id=self.pk, user_b_id=user_id)

    def is_staff_of_community(self, community_pk):
        return self.is_administrator_of_community(community_pk=community_pk) or self.is_moderator_of_community(community_pk=community_pk) or self.is_editor_of_community(community_pk=community_pk)

    def is_member_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk).exists()

    def is_voted_of_survey(self, survey_pk):
        return self.user_voter.filter(survey__pk=survey_pk).exists()

    def is_banned_from_community(self, community_pk):
        return self.banned_of_communities.filter(pk=community_pk).exists()

    def is_follow_from_community(self, community_pk):
        return self.community_follows.filter(community__pk=community_pk).exists()

    def is_creator_of_community(self, community_pk):
        return self.created_communities.filter(pk=community_pk).exists()

    def get_elect_subscribers_count(self):
        from elect.models import SubscribeElect
        return SubscribeElect.objects.filter(user_id=self.pk).values("pk").count()

    def get_like_news(self):
        from common.model.votes import ElectNewVotes2
        from blog.models import ElectNew

        likes = ElectNewVotes2.objects.filter(user_id=self.pk, vote=ElectNewVotes2.LIKE).values("new_id")
        news_ids = [new['new_id'] for new in likes]
        return ElectNew.objects.filter(id__in=news_ids)

    def get_like_news_count(self):
        from common.model.votes import ElectNewVotes2
        return ElectNewVotes2.objects.filter(user_id=self.pk, vote=ElectNewVotes2.LIKE).values("new_id").count()

    def get_dislike_news(self):
        from common.model.votes import ElectNewVotes2
        from blog.models import ElectNew

        dislikes = ElectNewVotes2.objects.filter(user_id=self.pk, vote=ElectNewVotes2.DISLIKE).values("new_id")
        news_ids = [new['new_id'] for new in dislikes]
        return ElectNew.objects.filter(id__in=news_ids)

    def get_dislike_news_count(self):
        from common.model.votes import ElectNewVotes2
        return ElectNewVotes2.objects.filter(user_id=self.pk, vote=ElectNewVotes2.DISLIKE).values("new_id").count()

    def is_suspended(self):
        return self.type[:4] == "_SUS"
    def is_have_warning_banner(self):
        return self.type[:4] == "_BAN"
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_manager(self):
        return self.type == User.MANAGER or self.is_superuser
    def is_supermanager(self):
        return self.type == User.SUPERMANAGER or self.is_superuser
    def is_identified_send(self):
        return self.type == User.IDENTIFIED_SEND
    def is_identified(self):
        return self.type == User.IDENTIFIED or self.is_superuser
    def is_deputat(self):
        return self.type == User.DEPUTAT
    def is_deputat_send(self):
        return self.type == User.DEPUTAT_SEND
    def is_no_phone_verified(self):
        return self.type == User.PHONE_NO_VERIFIED

    def is_man(self):
        return self.gender == User.MALE
    def is_women(self):
        return self.gender == User.FEMALE

    def is_staffed_user(self):
        return self.communities_memberships.filter(Q(is_administrator=True) | Q(is_moderator=True) | Q(is_editor=True)).exists()
    def is_administrator_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk, is_administrator=True).exists()
    def is_moderator_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk, is_moderator=True).exists()
    def is_advertiser_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk, is_advertiser=True).exists()
    def is_editor_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk, is_editor=True).exists()

    def has_blocked_user_with_id(self, user_id):
        return self.user_blocks.filter(blocked_user_id=user_id).exists()

    def is_blocked_user_with_id(self, user_id):
        return self.blocked_by_users.filter(blocked_user_id=user_id).exists()

    def is_connected_with_user_with_id(self, user_id):
        return self.connections.filter(target_connection__user_id=user_id).exists()

    def is_following_user_with_id(self, user_id):
        return self.follows.filter(followed_user__id=user_id).exists()
    def is_followers_user_with_id(self, user_id):
        return self.followers.filter(user__id=user_id).exists()
    def is_followers_user_view(self, user_id):
        return self.followers.filter(user__id=user_id, view=True).exists()

    def has_blocked_user_with_id(self, user_id):
        return self.user_blocks.filter(blocked_user_id=user_id).exists()

    def create_s_avatar(self, photo_input):
        from easy_thumbnails.files import get_thumbnailer

        self.s_avatar = photo_input
        self.save(update_fields=['s_avatar'])
        new_img = get_thumbnailer(self.s_avatar)['small_avatar'].url.replace('media/', '')
        self.s_avatar = new_img
        return self.save(update_fields=['s_avatar'])

    def get_avatar(self):
        try:
            return self.s_avatar.url
        except:
            return '/static/images/user.png'

    def get_last_activity(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.last_activity)

    def get_country(self):
        from users.model.profile import UserLocation
        return UserLocation.objects.filter(user_id=self.pk).last().country_ru

    def get_online_display(self):
        from datetime import datetime, timedelta

        now = datetime.now()
        onl = self.last_activity + timedelta(minutes=3)
        if self.device == User.DESCTOP:
            device = '&nbsp;<svg style="width: 17px;" class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M20 18c1.1 0 1.99-.9 1.99-2L22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2H0v2h24v-2h-4zM4 6h16v10H4V6z"/></svg>'
        else:
            device = '&nbsp;<svg style="width: 17px;" class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/></svg>'
        if now < onl:
            return '<i>Онлайн</i>' + device
        else:
            if self.is_women():
                return '<i>Была ' + self.get_last_activity() + '</i>' + device
            else:
                return '<i>Был ' + self.get_last_activity() + '</i>' + device

    def get_user_news_notify_ids(self):
        from notify.models import UserNewsNotify
        return [i['target'] for i in UserNewsNotify.objects.filter(user=self.pk).values('target')]

    def get_user_profile_notify_ids(self):
        from notify.models import UserProfileNotify
        return [i['target'] for i in UserProfileNotify.objects.filter(user=self.pk).values('target')]

    def get_user_notify(self):
        from notify.models import Notify
        query = Q(recipient_id=self.pk)|Q(creator_id__in=self.get_user_profile_notify_ids())
        query.add(Q(Q(user_set__isnull=True, object_set__isnull=True)|Q(status="U")), Q.AND)
        return Notify.objects.filter(query)

        query = Q(creator_id__in=self.get_user_profile_notify_ids())
        query.add(Q(user_set__isnull=True, object_set__isnull=True), Q.AND)
        query.add(Q(recipient_id=self.pk), Q.AND)
        return Notify.objects.only('created').filter(query)

    def read_user_notify(self):
        from notify.models import Notify
        Notify.u_notify_unread(self.pk)

    def count_unread_notify(self):
        from notify.models import Notify
        query = Q(recipient_id=self.pk, status="U")
        return Notify.objects.filter(query).values("pk").count()

    def unread_notify_count(self):
        count = self.count_unread_notify()
        if count > 0:
            return '<span class="tab_badge badge-success" style="font-size: 60%;">' + str(count) + '</span>'
        else:
            return ''

    def get_member_for_notify_ids(self):
        from notify.models import UserProfileNotify
        return [i['target'] for i in UserProfileNotify.objects.filter(user=self.pk).values("target")]

    def add_news_subscriber(self, user_id):
        from notify.models import UserNewsNotify
        if not UserNewsNotify.objects.filter(user=self.pk, target=user_id).exists():
            UserNewsNotify.objects.create(user=self.pk, target=user_id)
    def delete_news_subscriber(self, user_id):
        from notify.models import UserNewsNotify
        if UserNewsNotify.objects.filter(user=self.pk, target=user_id).exists():
            notify = UserNewsNotify.objects.get(user=self.pk, target=user_id).delete()

    def add_notify_subscriber(self, user_id):
        from notify.models import UserProfileNotify
        if not UserProfileNotify.objects.filter(user=self.pk, target=user_id).exists():
            UserProfileNotify.objects.create(user=self.pk, target=user_id)
    def delete_notify_subscriber(self, user_id):
        from notify.models import UserProfileNotify
        if UserProfileNotify.objects.filter(user=self.pk, target=user_id).exists():
            notify = UserProfileNotify.objects.get(user=self.pk, target=user_id).delete()

    def plus_carma(self, value, reason):
        from users.model.profile import UserTransaction, UserProfile
        from region.models import Region
        from district.models import District

        self.point += value
        self.save(update_fields=["point"])
        UserTransaction.objects.create(user_id=self.pk, reason=reason, value=value, total=self.point)
        profile = UserProfile.objects.get(user=self)
        profile.total_costs += value
        profile.save(update_fields=["total_costs"])
        district = self.area
        district.total_costs += value
        district.save(update_fields=["total_costs"])
        region = district.region
        region.total_costs += value
        region.save(update_fields=["total_costs"])

    def minus_carma(self, value, reason):
        from users.model.profile import UserTransaction, UserProfile
        from region.models import Region
        from district.models import District

        self.point -= value
        self.save(update_fields=["point"])
        UserTransaction.objects.create(user_id=self.pk, reason=reason, value=value, total=self.point)
        profile = UserProfile.objects.get(user=self)
        profile.total_revenue += value
        profile.save(update_fields=["total_revenue"])

        district = self.area
        district.total_revenue += value
        district.save(update_fields=["total_revenue"])
        region = district.region
        region.total_revenue += value
        region.save(update_fields=["total_revenue"])

    def get_age(self):
        from datetime import date
        from users.model.profile import UserProfile
        from django.utils.formats import localize

        try:
            user, today = UserProfile.objects.get(user_id=self.pk), date.today()
            age = today.year - user.birthday.year - ((today.month, today.day) < (user.birthday.month, user.birthday.day))
            return str(localize(user.birthday)) + " (" + str(age) + ")"
        except:
            return 'Не указано'

    def get_elect_new_views_for_year(self, year):
        from blog.models import ElectNew
        from common.model.comments import ElectNewComment
        from common.model.votes import ElectNewVotes2
        comments, likes, dislikes, inerts, auth_count, anon_count, posts = 0, 0, 0, 0, 0, ElectNew.objects.filter(creator_id=self.pk, type=ElectNew.PUBLISHED)
        for i in posts:
            views = ElectNewNumbers.objects.filter(new=i.pk, created__year=year)
            auth_count += views.exclude(user=0).values('pk').count()
            anon_count += views.filter(user=0).values('pk').count()

            comments += ElectNewComment.objects.filter(new=i.pk, created__year=year)

            votes = ElectNewVotes2.objects.filter(new=i.pk, created__year=year)
            likes += votes.filter(vote="LIK").values('pk').count()
            dislikes += votes.filter(vote="DIS").values('pk').count()
            inerts += votes.filter(vote="INE").values('pk').count()
        return [comments, likes, dislikes, inerts, auth_count, anon_count]
    def get_post_views_for_month(self, month):
        from blog.models import ElectNew
        from common.model.comments import ElectNewComment
        from common.model.votes import ElectNewVotes2
        comments, likes, dislikes, inerts, auth_count, anon_count, posts = 0, 0, 0, 0, 0, ElectNew.objects.filter(creator_id=self.pk, type=ElectNew.PUBLISHED)
        for i in posts:
            views = ElectNewNumbers.objects.filter(new=i.pk, created__month=month)
            auth_count += views.exclude(user=0).values('pk').count()
            anon_count += views.filter(user=0).values('pk').count()

            comments += ElectNewComment.objects.filter(new=i.pk, created__month=month)

            votes = ElectNewVotes2.objects.filter(new=i.pk, created__month=month)
            likes += votes.filter(vote="LIK").values('pk').count()
            dislikes += votes.filter(vote="DIS").values('pk').count()
            inerts += votes.filter(vote="INE").values('pk').count()
        return [comments, likes, dislikes, inerts, auth_count, anon_count]
    def get_post_views_for_week(self, week):
        from blog.models import ElectNew
        from common.model.comments import ElectNewComment
        from common.model.votes import ElectNewVotes2
        comments, likes, dislikes, inerts, auth_count, anon_count, posts = 0, 0, 0, 0, 0, ElectNew.objects.filter(creator_id=self.pk, type=ElectNew.PUBLISHED)
        for i in posts:
            views = ElectNewNumbers.objects.filter(new=i.pk, created__day__in=week)
            auth_count += views.exclude(user=0).values('pk').count()
            anon_count += views.filter(user=0).values('pk').count()

            comments += ElectNewComment.objects.filter(new=i.pk, created__day__in=week)

            votes = ElectNewVotes2.objects.filter(new=i.pk, created__day__in=week)
            likes += votes.filter(vote="LIK").values('pk').count()
            dislikes += votes.filter(vote="DIS").values('pk').count()
            inerts += votes.filter(vote="INE").values('pk').count()
        return [comments, likes, dislikes, inerts, auth_count, anon_count]
    def get_post_views_for_day(self, day):
        from blog.models import ElectNew
        from common.model.comments import ElectNewComment
        from common.model.votes import ElectNewVotes2
        comments, likes, dislikes, inerts, auth_count, anon_count, posts = 0, 0, 0, 0, 0, ElectNew.objects.filter(creator_id=self.pk, type=ElectNew.PUBLISHED)
        for i in posts:
            views = ElectNewNumbers.objects.filter(new=i.pk, created__day=day)
            auth_count += views.exclude(user=0).values('pk').count()
            anon_count += views.filter(user=0).values('pk').count()

            comments += ElectNewComment.objects.filter(new=i.pk, created__day=day)

            votes = ElectNewVotes2.objects.filter(new=i.pk, created__day=day)
            likes += votes.filter(vote="LIK").values('pk').count()
            dislikes += votes.filter(vote="DIS").values('pk').count()
            inerts += votes.filter(vote="INE").values('pk').count()
        return [comments, likes, dislikes, inerts, auth_count, anon_count]

    def get_transactions(self):
        from users.model.profile import UserTransaction
        return UserTransaction.objects.filter(user_id=self.pk)

    def get_transactions_count(self):
        from users.model.profile import UserTransaction
        return UserTransaction.objects.filter(user_id=self.pk).values("pk").count()

    def get_total_costs(self):
        from users.model.profile import UserTransaction
        from django.db.models import Sum

        transactions = UserTransaction.objects.filter(user_id=self.pk, reason="ADD")
        return transactions.aggregate(Sum('value'))['value__sum']

    def get_total_revenue(self):
        from users.model.profile import UserTransaction
        from django.db.models import Sum

        query = Q(user_id=self.pk)
        query.add(Q(Q(reason="PAY") | Q(reason="AUP") | Q(reason="PEN")), Q.AND)
        transactions = UserTransaction.objects.filter(query)
        return transactions.aggregate(Sum('value'))['value__sum']

    def get_first_number(self):
        from users.model.profile import UserLocation
        return UserLocation.objects.filter(user_id=self.pk).last().phone

    def get_photo_lists(self):
        from gallery.models import PhotoList
        return PhotoList.objects.filter(~Q(type__contains="_")&Q(creator_id=self.pk))

    def get_doc_lists(self):
        from docs.models import DocList
        return DocList.objects.filter(~Q(type__contains="_")&Q(creator_id=self.pk))

    def get_playlists(self):
        from music.models import SoundList
        return SoundList.objects.filter(~Q(type__contains="_")&Q(creator_id=self.pk))

    def get_video_lists(self):
        from video.models import VideoList
        return VideoList.objects.filter(~Q(type__contains="_")&Q(creator_id=self.pk))

    def get_survey_lists(self):
        from survey.models import SurveyList
        return SurveyList.objects.filter(~Q(type__contains="_")&Q(creator_id=self.pk))

    def get_unread_notify_count(self):
        count = self.notifications.filter(status="U").values("pk").count()
        if count:
            return count
        else:
            return''

    def get_blocked_users(self):
        return User.objects.filter(blocked_by_users__blocker_id=self.pk).distinct()

    def get_staffed_communities(self):
        from communities.models import Community

        query = Q(Q(memberships__user=self, memberships__is_administrator=True) | Q(memberships__user=self, memberships__is_editor=True))
        return Community.objects.filter(query)

    def unblock_user_with_pk(self, pk):
        user = User.objects.get(pk=pk)
        self.get_or_create_possible_friend(user)
        return self.unblock_user_with_id(user_id=user.pk)

    def unblock_user_with_id(self, user_id):
        check_can_unblock_user(user=self, user_id=user_id)
        self.user_blocks.filter(blocked_user_id=user_id).delete()
        return User.objects.get(pk=user_id)

    def block_user_with_pk(self, pk):
        user = User.objects.get(pk=pk)
        return self.block_user_with_id(user_id=user.pk)

    def block_user_with_id(self, user_id):
        from users.model.profile import UserBlock
        from common.check.user import check_can_block_user
        check_can_block_user(user=self, user_id=user_id)

        if self.is_connected_with_user_with_id(user_id=user_id):
            self.disconnect_from_user_with_id(user_id=user_id)
        if self.is_following_user_with_id(user_id=user_id):
            self.unfollow_user_with_id(user_id=user_id)

        user_to_block = User.objects.get(pk=user_id)
        if user_to_block.is_following_user_with_id(user_id=self.pk):
            user_to_block.unfollow_user_with_id(self.pk)

        UserBlock.create_user_block(blocker_id=self.pk, blocked_user_id=user_id)
        self.remove_possible_friend(user_id)
        self.delete_news_subscriber(user_id)
        self.delete_profile_subscriber(user_id)
        return user_to_block

    def disconnect_from_user_with_id(self, user_id):
        from common.check.user import check_is_connected
        check_is_connected(user=self, user_id=user_id)
        if self.is_following_user_with_id(user_id):
            self.unfollow_user_with_id(user_id)
        connection = self.connections.get(target_connection__user_id=user_id)
        connection.delete()

    def unfollow_user(self, user):
        self.unfollow_user_with_id(user.pk)
        return user.minus_follows(1)

    def unfollow_user_with_id(self, user_id):
        from users.model.profile import Follow
        from common.check.user import check_not_can_follow_user
        check_not_can_follow_user(user=self, user_id=user_id)
        follow = Follow.objects.get(user=self,followed_user_id=user_id).delete()
        self.delete_news_subscriber(user_id)

    def follow_user(self, user):
        self.follow_user_with_id(user.pk)
        user.plus_follows(1)

    def follow_user_with_id(self, user_id):
        from users.model.profile import Follow
        from common.check.user import check_can_follow_user

        check_can_follow_user(user_id=user_id, user=self)
        if self.pk == user_id:
            raise ValidationError('Вы не можете подписаться сами на себя',)
        #elif not self.is_closed_profile():
        self.add_news_subscriber(user_id)
        return Follow.create_follow(user_id=self.pk, followed_user_id=user_id)

    def community_follow_user(self, community_pk):
        return self.follow_community(community_pk)

    def follow_community(self, community):
        from communities.models import CommunityFollow
        from common.check.user import check_can_join_community

        check_can_join_community(user=self, community_pk=community.pk)
        if community.is_public():
            community.add_news_subscriber(self.pk)
        return CommunityFollow.create_follow(user_id=self.pk, community_pk=community_pk)

    def community_unfollow_user(self, community):
        return self.unfollow_community(community)

    def unfollow_community(self, community):
        from communities.models import CommunityFollow
        from common.check.user import check_can_join_community

        check_can_join_community(user=self, community_pk=community.pk)
        follow = CommunityFollow.objects.get(user=self,community__pk=community.pk).delete()
        community.delete_news_subscriber(self.pk)

    def join_community(self, community):
        from communities.models import Community, CommunityFollow
        from common.check.user import check_can_join_community

        check_can_join_community(user=self, community_id=community.pk)
        community_to_join = Community.objects.get(pk=community.pk)
        community_to_join.add_member(self)
        if community_to_join.is_private():
            CommunityInvite.objects.filter(community_pk=community.pk, invited_user__id=self.id).delete()
        elif community_to_join.is_closed():
            CommunityFollow.objects.filter(community__pk=community.pk, user__id=self.id).delete()
        return community_to_join

    def leave_community(self, community):
        from common.check.user import check_can_join_community

        check_can_leave_community(user=self, community_id=community.pk)
        return community.remove_member(self)

    def get_vote_of_survey(self, survey_pk):
        return self.user_voter.filter(survey__pk=survey_pk)[0]

    def is_user_administrator(self):
        return self.is_superuser or try_except(self.user_staff.level == "A")
    def is_user_moderator(self):
        return self.is_superuser or try_except(self.user_staff.level == "M")
    def is_user_editor(self):
        return self.is_superuser or try_except(self.user_staff.level == "E")
    def is_user_advertiser(self):
        return self.is_superuser or try_except(self.user_staff.level == "R")
    def is_user_manager(self):
        try:
            return self.is_superuser or (self.user_staff.level and self.user_staff.level != "R")
        except:
            return False

    def is_community_administrator(self):
        return self.is_superuser or try_except(self.user_community_staff.level == "A")
    def is_community_moderator(self):
        return self.is_superuser or try_except(self.user_community_staff.level == "M")
    def is_community_editor(self):
        return self.is_superuser or try_except(self.user_community_staff.level == "E")
    def is_community_advertiser(self):
        return self.is_superuser or try_except(self.user_community_staff.level == "R")
    def is_community_manager(self):
        try:
            return self.is_superuser or (self.user_community_staff.level and self.user_community_staff.level != "R")
        except:
            return False

    def is_elect_new_administrator(self):
        return self.is_superuser or try_except(self.elect_new_user_staff.level == "A")
    def is_elect_new_moderator(self):
        return self.is_superuser or try_except(self.elect_new_user_staff.level == "M")
    def is_elect_new_editor(self):
        return self.is_superuser or try_except(self.elect_new_user_staff.level == "E")
    def is_elect_new_manager(self):
        try:
            return self.is_superuser or self.elect_new_user_staff.level
        except:
            return False

    def is_blog_administrator(self):
        return self.is_superuser or try_except(self.blog_user_staff.level == "A")
    def is_blog_moderator(self):
        return self.is_superuser or try_except(self.blog_user_staff.level == "M")
    def is_blog_editor(self):
        return self.is_superuser or try_except(self.blog_user_staff.level == "E")
    def is_blog_manager(self):
        try:
            return self.is_superuser or self.blog_user_staff.level
        except:
            return False

    def is_survey_administrator(self):
        return self.is_superuser or try_except(self.survey_user_staff.level == "A")
    def is_survey_moderator(self):
        return self.is_superuser or try_except(self.survey_user_staff.level == "M")
    def is_survey_editor(self):
        return self.is_superuser or try_except(self.survey_user_staff.level == "E")
    def is_survey_manager(self):
        try:
            return self.is_superuser or self.survey_user_staff.level
        except:
            return False

    def is_doc_administrator(self):
        return self.is_superuser or try_except(self.doc_user_staff.level == "A")
    def is_doc_moderator(self):
        return self.is_superuser or try_except(self.doc_user_staff.level == "M")
    def is_doc_editor(self):
        return self.is_superuser or try_except(self.doc_user_staff.level == "E")
    def is_doc_manager(self):
        try:
            return self.is_superuser or self.doc_user_staff.level
        except:
            return False


    def is_photo_administrator(self):
        return self.is_superuser or try_except(self.photo_user_staff.level == "A")
    def is_photo_moderator(self):
        return self.is_superuser or try_except(self.photo_user_staff.level == "M")
    def is_photo_editor(self):
        return self.is_superuser or try_except(self.photo_user_staff.level == "E")
    def is_photo_manager(self):
        try:
            return self.is_superuser or self.photo_user_staff.level
        except:
            return False

    def is_video_administrator(self):
        return self.is_superuser or try_except(self.video_user_staff.level == "A")
    def is_video_moderator(self):
        return self.is_superuser or try_except(self.video_user_staff.level == "M")
    def is_video_editor(self):
        return self.is_superuser or try_except(self.video_user_staff.level == "E")
    def is_video_manager(self):
        try:
            return self.is_superuser or self.video_user_staff.level
        except:
            return False

    def is_audio_administrator(self):
        return self.is_superuser or try_except(self.music_user_staff.level == "A")
    def is_audio_moderator(self):
        return self.is_superuser or try_except(self.music_user_staff.level == "M")
    def is_audio_editor(self):
        return self.is_superuser or try_except(self.music_user_staff.level == "E")
    def is_audio_manager(self):
        try:
            return self.is_superuser or self.music_user_staff.level
        except:
            return False

    def is_organization_administrator(self):
        return self.is_superuser or try_except(self.organization_user_staff.level == "A")
    def is_organization_moderator(self):
        return self.is_superuser or try_except(self.organization_user_staff.level == "M")
    def is_organization_editor(self):
        return self.is_superuser or try_except(self.organization_user_staff.level == "E")
    def is_organization_manager(self):
        try:
            return self.is_superuser or self.organization_user_staff.level
        except:
            return False

    def is_work_organization_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_organization.can_work_administrator)
    def is_work_organization_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_organization.can_work_moderator)
    def is_work_organization_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_organization.can_work_editor)
    def is_work_organization_advertiser(self):
        return self.is_superuser or try_except(self.can_work_staff_organization.can_work_advertiser)
    def is_organization_supermanager(self):
        return self.is_work_organization_administrator() or self.is_work_organization_moderator() or is_work_organization_editor() or is_work_organization_advertiser()

    def is_work_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_user.can_work_administrator)
    def is_work_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_user.can_work_moderator)
    def is_work_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_user.can_work_editor)
    def is_work_advertiser(self):
        return self.is_superuser or try_except(self.can_work_staff_user.can_work_advertiser)
    def is_user_supermanager(self):
        return self.is_work_administrator() or self.is_work_moderator() or is_work_editor() or is_work_advertiser()

    def is_work_community_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_community.can_work_administrator)
    def is_work_community_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_community.can_work_moderator)
    def is_work_community_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_community.can_work_editor)
    def is_work_community_advertiser(self):
        return self.is_superuser or try_except(self.can_work_staff_community.can_work_advertiser)
    def is_community_supermanager(self):
        return self.is_work_community_administrator() or self.is_work_community_moderator() or is_work_community_editor() or is_work_community_advertiser()

    def is_work_elect_new_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_elect_new_user.can_work_administrator)
    def is_work_elect_new_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_elect_new_user.can_work_moderator)
    def is_work_elect_new_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_elect_new_user.can_work_editor)
    def is_work_supermanager(self):
        return self.is_work_elect_new_administrator() or self.is_work_elect_new_moderator() or is_work_elect_new_editor()

    def is_work_blog_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_blog_user.can_work_administrator)
    def is_work_blog_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_blog_user.can_work_moderator)
    def is_work_blog_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_blog_user.can_work_editor)
    def is_work_supermanager(self):
        return self.is_work_blog_administrator() or self.is_work_blog_moderator() or is_work_blog_editor()

    def is_work_survey_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_survey_user.can_work_administrator)
    def is_work_survey_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_survey_user.can_work_moderator)
    def is_work_survey_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_survey_user.can_work_editor)
    def is_work_supermanager(self):
        return self.is_work_survey_administrator() or self.is_work_survey_moderator() or is_work_survey_editor()

    def is_work_doc_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_doc_user.can_work_administrator)
    def is_work_doc_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_doc_user.can_work_moderator)
    def is_work_doc_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_doc_user.can_work_editor)
    def is_work_doc_supermanager(self):
        return self.is_work_doc_administrator() or self.is_doc_good_moderator() or is_work_doc_editor()

    def is_work_photo_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_photo_user.can_work_administrator)
    def is_work_photo_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_photo_user.can_work_moderator)
    def is_work_photo_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_photo_user.can_work_editor)
    def is_work_photo_supermanager(self):
        return self.is_work_photo_administrator() or self.is_work_photo_moderator() or is_work_photo_editor()

    def is_work_video_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_video_user.can_work_administrator)
    def is_work_video_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_video_user.can_work_moderator)
    def is_work_video_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_video_user.can_work_editor)
    def is_work_video_supermanager(self):
        return self.is_work_video_administrator() or self.is_work_video_moderator() or is_work_video_editor()

    def is_work_music_administrator(self):
        return self.is_superuser or try_except(self.can_work_staff_music_user.can_work_administrator) or self.is_superuser
    def is_work_music_moderator(self):
        return self.is_superuser or try_except(self.can_work_staff_music_user.can_work_moderator) or self.is_superuser
    def is_work_music_editor(self):
        return self.is_superuser or try_except(self.can_work_staff_music_user.can_work_editor) or self.is_superuser
    def is_music_supermanager(self):
        return self.is_work_music_administrator() or self.is_work_music_moderator() or is_work_music_editor()

    def is_no_view_followers(self):
        return self.followers.filter(view=False).exists()

    def is_have_followers(self):
        return self.profile.follows > 0
    def is_have_followings(self):
        return self.follows.values('pk').exists()
    def is_have_blacklist(self):
        return self.user_blocks.values('pk').exists()
    def is_have_friends(self):
        return self.profile.friends > 0
    def is_have_communities(self):
        return self.profile.communities > 0
    def is_have_music(self):
        return self.profile.tracks > 0

    def count_no_view_followers(self):
        return self.followers.filter(view=False).values('pk').count()
    def count_following(self):
        return self.follows.values('pk').count()
    def count_followers(self):
        return self.user_info.follows
    def count_blacklist(self):
        return self.user_blocks.values('pk').count()
    def count_photos(self):
        return self.user_info.photos
    def count_docs(self):
        return self.user_info.docs
    def count_surveys(self):
        return self.user_info.surveys
    def count_elect_news(self):
        return self.user_info.elect_news
    def count_communities(self):
        return self.user_info.communities
    def count_tracks(self):
        return self.user_info.tracks
    def count_videos(self):
        return self.user_info.videos
    def count_friends(self):
        return self.user_info.friends

    def plus_photos(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.photos += count
        return profile.save(update_fields=['photos'])
    def minus_photos(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.photos -= count
            return profile.save(update_fields=['photos'])
        except:
            pass
    def plus_elect_news(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.elect_news += count
        return profile.save(update_fields=['elect_news'])
    def minus_elect_news(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.elect_news += count
            return profile.save(update_fields=['elect_news'])
        except:
            pass
    def plus_surveys(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.surveys += count
        return profile.save(update_fields=['surveys'])
    def minus_surveys(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.surveys -= count
            return profile.save(update_fields=['surveys'])
        except:
            pass
    def plus_videos(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.videos += count
        return profile.save(update_fields=['videos'])
    def minus_videos(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.videos -= count
            return profile.save(update_fields=['videos'])
        except:
            pass
    def plus_docs(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.docs += count
        return profile.save(update_fields=['docs'])
    def minus_docs(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.docs -= count
            return profile.save(update_fields=['docs'])
        except:
            pass
    def plus_tracks(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.tracks += count
        return profile.save(update_fields=['tracks'])
    def minus_tracks(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.tracks -= count
            return profile.save(update_fields=['tracks'])
        except:
            pass
    def plus_communities(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.communities += count
        return profile.save(update_fields=['communities'])
    def minus_communities(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.communities -= count
            return profile.save(update_fields=['communities'])
        except:
            pass
    def plus_friends(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.friends += count
        return profile.save(update_fields=['friends'])
    def minus_friends(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.friends -= count
            return profile.save(update_fields=['friends'])
        except:
            pass
    def plus_follows(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.follows += count
        return profile.save(update_fields=['follows'])
    def minus_follows(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.follows -= count
            return profile.save(update_fields=['follows'])
        except:
            pass
    def plus_comments(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        profile.comments += count
        return profile.save(update_fields=['comments'])
    def minus_comments(self, count):
        from users.model.profile import UserProfile
        profile = UserProfile.objects.get(user=self)
        try:
            profile.comments -= count
            return profile.save(update_fields=['comments'])
        except:
            pass

    def get_default_communities(self):
        from communities.models import Community
        return Community.objects.filter(memberships__user_id=self.pk)

    def get_6_default_communities(self):
        from communities.models import Community
        return Community.objects.filter(memberships__user=self)[0:6]

    def get_longest_user_penalties(self):
        from managers.models import ModerationPenalty
        return ModerationPenalty.objects.filter(object_id=self.pk, type="USE")[0].expiration
    def get_moderated_description(self):
        from managers.models import Moderated
        return Moderated.objects.filter(object_id=self.pk, type="USE")[0].description
