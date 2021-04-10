from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from common.utils import try_except
from users.helpers import upload_to_user_directory
from city.models import City

"""
    Группируем все таблицы пользователя здесь:
    1. Сам пользователь
"""

class User(AbstractUser):
    DELETED, SUSPENDED, BLOCKED, PHONE_NO_VERIFIED, STANDART, MANAGER, SUPERMANAGER = 'DE', 'SU', 'BL', 'PV', 'ST', 'MA', 'SM'
    MALE, FEMALE, DESCTOP, PHONE = 'Man', 'Fem', 'De', 'Ph'
    PERM = (
        (DELETED, 'Удален'),
        (BLOCKED, 'Заблокирован'),
        (PHONE_NO_VERIFIED, 'Телефон не подтвержден'),
        (STANDART, 'Обычные права'),
        (MANAGER, 'Менеджер'),
        (SUPERMANAGER, 'Суперменеджер'),
    )
    GENDER, DEVICE = ((MALE, 'Мужской'),(FEMALE, 'Женский'),), ((DESCTOP, 'Комп'),(PHONE, 'Телефон'),)

    last_activity = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Активность')
    phone = models.CharField(max_length=17, unique=True, verbose_name='Телефон')
    perm = models.CharField(max_length=5, choices=PERM, default=PHONE_NO_VERIFIED, verbose_name="Уровень доступа")
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    gender = models.CharField(max_length=5, choices=GENDER, blank=True, verbose_name="Пол")
    device = models.CharField(max_length=5, choices=DEVICE, blank=True, verbose_name="Оборудование")
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL, verbose_name="Город")
    point = models.PositiveIntegerField(default=0, verbose_name="Количество кармы")
    level = models.PositiveSmallIntegerField(default=1, verbose_name="Уровень")
    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.get_full_name()

    def get_verb_gender(self, verb):
        if self.is_women():
            return "W" + verb
        else:
            return verb

    def get_full_name_genitive(self):
        import pymorphy2
        from string import ascii_letters

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

    def get_or_create_main_album(self):
        from gallery.models import Album
        try:
            album = Album.objects.get(creator_id=self.pk, type=Album.MAIN)
        except:
            album = Album.objects.create(creator_id=self.pk, type=Album.MAIN, title="Прикреплённые фото", description="Прикреплённые фото", order=0)
        return album
    def get_or_create_main_doclist(self):
        from docs.models import DocList
        try:
            album = DocList.objects.get(creator_id=self.pk, type=DocList.MAIN)
        except:
            album = DocList.objects.create(creator_id=self.pk, type=DocList.MAIN, name="Основной список", order=0)
        return album
    def get_or_create_main_playlist(self):
        from music.models import SoundList
        try:
            list = SoundList.objects.get(creator_id=self.pk, type=SoundList.MAIN)
        except:
            list = SoundList.objects.create(creator_id=self.pk, type=SoundList.MAIN, name="Основной список", order=0)
        return list
    def get_or_create_main_videolist(self):
        from video.models import VideoAlbum
        try:
            list = VideoAlbum.objects.get(creator_id=self.pk, type=VideoAlbum.MAIN)
        except:
            list = VideoAlbum.objects.create(creator_id=self.pk, type=VideoAlbum.MAIN, title="Основной список", order=0)
        return list

    def get_full_name(self):
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
        if now < onl:
            return True
        else:
            return False

    def get_news(self):
        from blog.models import ElectNew
        return ElectNew.objects.filter(creator_id=self.pk)

    def get_news_count(self):
        from blog.models import ElectNew
        return ElectNew.objects.filter(creator_id=self.pk).values("pk").count()

    def get_elect_subscribers(self):
        from elect.models import Elect, SubscribeElect

        elect_subscribers = SubscribeElect.objects.filter(user_id=self.pk).values("elect_id")
        elect_ids = [elect['elect_id'] for elect in elect_subscribers]
        return Elect.objects.filter(id__in=elect_ids)

    def is_have_elect_subscribers(self):
        from elect.models import Elect, SubscribeElect

        elect_subscribers = SubscribeElect.objects.filter(user_id=self.pk).values("elect_id")
        elect_ids = [elect['elect_id'] for elect in elect_subscribers]
        return Elect.objects.filter(id__in=elect_ids).exists()

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

    def is_deleted(self):
        return try_except(self.perm == User.DELETED)
    def is_blocked(self):
        return try_except(self.perm == User.BLOCKED)
    def is_manager(self):
        return try_except(self.perm == User.MANAGER)
    def is_supermanager(self):
        return try_except(self.perm == User.SUPERMANAGER)
    def is_no_phone_verified(self):
        return try_except(self.perm == User.PHONE_NO_VERIFIED)
    def is_suspended(self):
        return try_except(self.perm == User.SUSPENDED)

    def is_man(self):
        if self.gender == User.MALE:
            return True
        else:
            return False
    def is_women(self):
        if self.gender == User.FEMALE:
            return True
        else:
            return False

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

        query = Q(creator_id__in=self.get_user_profile_notify_ids())
        query.add(Q(user_set__isnull=True, object_set__isnull=True), Q.AND)
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
            notify = UserNewsNotify.objects.get(user=self.pk, target=user_id)
            notify.delete()

    def add_notify_subscriber(self, user_id):
        from notify.models import UserProfileNotify
        if not UserProfileNotify.objects.filter(user=self.pk, target=user_id).exists():
            UserProfileNotify.objects.create(user=self.pk, target=user_id)
    def delete_notify_subscriber(self, user_id):
        from notify.models import UserProfileNotify
        if UserProfileNotify.objects.filter(user=self.pk, target=user_id).exists():
            notify = UserProfileNotify.objects.get(user=self.pk, target=user_id)
            notify.delete()

    def plus_carma(self, value, reason):
        from users.model.profile import UserTransaction

        self.point += value
        self.save(update_fields=["point"])
        UserTransaction.objects.create(user_id=self.pk, reason=reason, value=value, total=self.point)

    def minus_carma(self, value, reason):
        from users.model.profile import UserTransaction

        self.point -= value
        self.save(update_fields=["point"])
        UserTransaction.objects.create(user_id=self.pk, reason=reason, value=value, total=self.point)

    def get_age(self):
        from datetime import date
        from users.model.profile import UserInfo
        from django.utils.formats import localize

        try:
            user, today = UserInfo.objects.get(user_id=self.pk), date.today()
            age = today.year - user.birthday.year - ((today.month, today.day) < (user.birthday.month, user.birthday.day))
            return str(localize(user.birthday)) + " (" + str(age) + ")"
        except:
            return 'Не указано'

    def get_elect_new_views_for_year(self, year):
        from blog.models import ElectNew
        from common.model.comments import ElectNewComment
        from common.model.votes import ElectNewVotes2
        comments, likes, dislikes, inerts, auth_count, anon_count, posts = 0, 0, 0, 0, 0, ElectNew.objects.filter(creator_id=self.pk, status=ElectNew.STATUS_PUBLISHED)
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
        comments, likes, dislikes, inerts, auth_count, anon_count, posts = 0, 0, 0, 0, 0, ElectNew.objects.filter(creator_id=self.pk, status=ElectNew.STATUS_PUBLISHED)
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
        comments, likes, dislikes, inerts, auth_count, anon_count, posts = 0, 0, 0, 0, 0, ElectNew.objects.filter(creator_id=self.pk, status=ElectNew.STATUS_PUBLISHED)
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
        comments, likes, dislikes, inerts, auth_count, anon_count, posts = 0, 0, 0, 0, 0, ElectNew.objects.filter(creator_id=self.pk, status=ElectNew.STATUS_PUBLISHED)
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

    def get_my_albums(self):
        from gallery.models import Album
        albums_query = Q(type="LIS") | Q(type="PRI")
        albums_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return Album.objects.filter(albums_query)
    def is_have_my_albums(self):
        from gallery.models import Album
        albums_query = Q(type="LIS") | Q(type="PRI")
        albums_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return Album.objects.filter(albums_query).exists()
    def get_albums(self):
        from gallery.models import Album
        albums_query = Q(type="LIS")
        albums_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return Album.objects.filter(albums_query).order_by("order")
    def is_have_albums(self):
        from gallery.models import Album
        albums_query = Q(type="LIS")
        albums_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return Album.objects.filter(albums_query).exists()

    def get_my_all_doc_lists(self):
        from docs.models import DocList
        docs_query = Q(type="LIS") | Q(type="PRI") | Q(type="MAI")
        docs_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return DocList.objects.filter(docs_query)
    def is_have_my_all_doc_lists(self):
        from docs.models import DocList
        docs_query = Q(type="LIS") | Q(type="PRI") | Q(type="MAI")
        docs_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return DocList.objects.filter(docs_query).exists()
    def get_my_doc_lists(self):
        from docs.models import DocList
        docs_query = Q(type="LIS") | Q(type="PRI")
        docs_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return DocList.objects.filter(docs_query)
    def is_have_my_doc_lists(self):
        from docs.models import DocList
        docs_query = Q(type="LIS") | Q(type="PRI")
        docs_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return DocList.objects.filter(docs_query).exists()
    def get_doc_lists(self):
        from docs.models import DocList
        docs_query = Q(type="LIS")
        docs_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return DocList.objects.filter(docs_query).order_by("order")
    def is_have_doc_lists(self):
        from docs.models import DocList
        docs_query = Q(type="LIS")
        docs_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return DocList.objects.filter(docs_query).exists()
    def count_doc_lists(self):
        from docs.models import DocList
        docs_query = Q(type="LIS")
        docs_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return DocList.objects.filter(docs_query).values("pk").count()

    def get_my_playlists(self):
        from music.models import SoundList
        tracks_query = Q(type="LIS") | Q(type="PRI")
        tracks_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return SoundList.objects.filter(tracks_query)
    def is_have_my_playlists(self):
        from music.models import SoundList
        tracks_query = Q(type="LIS") | Q(type="PRI")
        tracks_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return SoundList.objects.filter(tracks_query).exists()
    def get_playlists(self):
        from music.models import SoundList
        tracks_query = Q(type="LIS")
        tracks_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return SoundList.objects.filter(tracks_query).order_by("order")
    def is_have_playlists(self):
        from music.models import SoundList
        tracks_query = Q(type="LIS")
        tracks_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return SoundList.objects.filter(tracks_query).exists()

    def get_my_video_lists(self):
        from video.models import VideoAlbum
        video_query = Q(type="LIS") | Q(type="PRI")
        video_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return VideoAlbum.objects.filter(video_query)
    def is_have_my_video_lists(self):
        from video.models import VideoAlbum
        video_query = Q(type="LIS") | Q(type="PRI")
        video_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return VideoAlbum.objects.filter(video_query).exists()
    def get_video_lists(self):
        from video.models import VideoAlbum
        video_query = Q(type="LIS")
        video_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return VideoAlbum.objects.filter(video_query).order_by("order")
    def is_have_video_lists(self):
        from video.models import VideoAlbum
        video_query = Q(type="LIS")
        video_query.add(Q(Q(creator_id=self.id)|Q(users__id=self.pk)), Q.AND)
        return VideoAlbum.objects.filter(video_query).exists()
