from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from region.models import Region
from django.db.models import Q


"""
    Группируем все таблицы о чиновниках здесь:
    1. Таблица чиновника,
    2. Таблица ссылки чиновника, много ссылок к одному чиновнику
    3. Таблица образования чиновника, много дипломов к одному чиновнику
    4. Таблица подписки пользователя на чиновника
"""

class Elect(models.Model):
    name = models.CharField(max_length=255, verbose_name="ФИО")
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 90}, upload_to="elect/%Y/%m/%d/", processors=[Transpose(), ResizeToFit(width=500, upscale=False)], verbose_name="Аватар")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    list = models.ManyToManyField('lists.AuthorityList', blank=True, related_name='elect_list', verbose_name="Орган гос. власти")
    region = models.ManyToManyField(Region, blank=True, related_name='elect_region', verbose_name="Регион, за которым закреплен депутат")
    birthday = models.CharField(max_length=100, null=True, verbose_name='Дата рождения')
    authorization = models.CharField(max_length=100, null=True, verbose_name='Дата наделения полномочиями')
    term_of_office = models.CharField(max_length=100, null=True, verbose_name='Срок окончания полномочий')
    election_information = models.CharField(max_length=200, blank=True, verbose_name="Сведения об избрании")
    fraction = models.ForeignKey('lists.Fraction', null=True, on_delete=models.SET_NULL, blank=True, verbose_name="Фракции")

    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    inert = models.PositiveIntegerField(default=0, verbose_name="Кол-во inert")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        verbose_name = "Чиновник"
        verbose_name_plural = "Чиновники"

    def __str__(self):
        return self.name

    def get_region_image(self):
        if self.region.all()[0].image:
            return self.region.all()[0].image.url
        else:
            return '/static/images/timeline.jpg'

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/static/images/no_photo.jpg'

    def get_first_list(self):
        return self.list.all()[0]

    def get_regions(self):
        regions = self.region.all()
        return regions

    def get_news(self):
        return self.new_elect.filter(type="PUB")

    def get_last_news(self):
        return self.new_elect.filter(type="PUB")[:6]

    def get_remote_image(self, image_url):
        import os
        from django.core.files import File
        from urllib import request

        result = request.urlretrieve(image_url)
        self.image.save(
            os.path.basename(image_url),
            File(open(result[0], 'rb'))
        )
        self.save()

    def visits_count(self):
        if self.view > 0:
            return self.view
        else:
            return ''

    def likes_count(self):
        if self.like > 0:
            return self.like
        else:
            return ''
    def dislikes_count(self):
        if self.dislike > 0:
            return self.dislike
        else:
            return ''
    def inerts_count(self):
        if self.inert > 0:
            return self.inert
        else:
            return ''
    def likes(self):
        from common.model.votes import ElectVotes
        return ElectVotes.objects.filter(elect_id=self.pk, vote="LIK")
    def dislikes(self):
        from common.model.votes import ElectVotes
        return ElectVotes.objects.filter(elect_id=self.pk, vote="DIS")
    def inerts(self):
        from common.model.votes import ElectVotes
        return ElectVotes.objects.filter(elect_id=self.pk, vote="INE")

    def is_have_likes(self):
        return self.like > 0
    def is_have_dislikes(self):
        return self.dislike > 0
    def is_have_inerts(self):
        return self.inert > 0

    def get_avatar(self):
        try:
            return self.image.url
        except:
            return '/static/images/user.png'

    def get_subscribers_ids(self):
        from users.models import User
        subscribers = SubscribeElect.objects.filter(elect_id=self.pk).values("user_id")
        return [i['user_id'] for i in subscribers]

    def get_subscribers(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_subscribers_ids())

    def is_have_subscribers(self):
        from users.models import User
        subscribers = SubscribeElect.objects.filter(elect_id=self.pk).values("user_id")
        user_ids = [i['user_id'] for i in subscribers]
        return User.objects.filter(id__in=user_ids).exists()

    def send_like(self, user):
        import json
        from common.model.votes import ElectVotes
        from django.http import HttpResponse
        try:
            item = ElectVotes.objects.get(elect=self, user=user)
            if item.vote == ElectVotes.DISLIKE:
                item.vote = ElectVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            elif item.vote == ElectVotes.INERT:
                item.vote = ElectVotes.LIKE
                item.save(update_fields=['vote'])
                self.inert -= 1
                self.like += 1
                self.save(update_fields=['inert', 'like'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(elect=self, user=user, vote=ElectVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            from common.notify.notify import user_notify, user_wall
            user_notify(user, None, self.pk, "ELE", "u_elec_notify", "LIK")
            user_wall(user, None, self.pk, "ELE", "u_elec_notify", "LIK")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count()),"inert_count": str(self.inerts_count())}),content_type="application/json")

    def send_dislike(self, user):
        import json
        from common.model.votes import ElectVotes
        from django.http import HttpResponse
        try:
            item = ElectVotes.objects.get(elect=self, user=user)
            if item.vote == ElectVotes.LIKE:
                item.vote = ElectVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            elif item.vote == ElectVotes.INERT:
                item.vote = ElectVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.inert -= 1
                self.dislike += 1
                self.save(update_fields=['inert', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(elect=self, user=user, vote=ElectVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            from common.notify.notify import user_notify, user_wall
            user_notify(user, None, self.pk, "ELE", "u_elec_notify", "DIS")
            user_wall(user, None, self.pk, "ELE", "u_elec_notify", "DIS")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count()),"inert_count": str(self.inerts_count())}),content_type="application/json")

    def send_inert(self, user):
        import json
        from common.model.votes import ElectVotes
        from django.http import HttpResponse
        try:
            item = ElectVotes.objects.get(elect=self, user=user)
            if item.vote == ElectVotes.LIKE:
                item.vote = ElectVotes.INERT
                item.save(update_fields=['vote'])
                self.like -= 1
                self.inert += 1
                self.save(update_fields=['like', 'inert'])
            elif item.vote == ElectVotes.DISLIKE:
                item.vote = ElectVotes.INERT
                item.save(update_fields=['vote'])
                self.inert += 1
                self.dislike -= 1
                self.save(update_fields=['inert', 'dislike'])
            else:
                item.delete()
                self.inert -= 1
                self.save(update_fields=['inert'])
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(elect=self, user=user, vote=ElectVotes.INERT)
            self.inert += 1
            self.save(update_fields=['inert'])
            from common.notify.notify import user_notify, user_wall
            user_notify(user, None, self.pk, "ELE", "u_elec_notify", "INE")
            user_wall(user, None, self.pk, "ELE", "u_elec_notify", "INE")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count()),"inert_count": str(self.inerts_count())}),content_type="application/json")


class LinkElect(models.Model):
    title = models.CharField(max_length=255, verbose_name="Текст ссылки")
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE, blank=True, verbose_name="Чиновник")
    link = models.URLField(max_length=255, verbose_name="Ссылки")

    class Meta:
        verbose_name = "Ссылка для чиновника"
        verbose_name_plural = "Ссылки"

    def __str__(self):
        return self.title


class EducationElect(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE, blank=True, verbose_name="Чиновник")
    year = models.CharField(max_length=10, verbose_name="Год")

    class Meta:
        verbose_name = "Образование чиновника"
        verbose_name_plural = "Образование"

    def __str__(self):
        return self.title


class SubscribeElect(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_subscribe', verbose_name="Пользователь")
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE, related_name='elect_subscribe', verbose_name="Чиновник")

    @classmethod
    def create_elect_subscribe(cls, user_id, elect_id):
        return cls.objects.create(user_id=user_id, elect_id=elect_id)

    @classmethod
    def is_elect_subscribe(cls, elect_id, user_id):
        return cls.objects.filter(Q(elect_id=elect_id, user_id=user_id)).exists()

    class Meta:
        unique_together = ('elect', 'user',)
        indexes = [models.Index(fields=['elect', 'user']),]
