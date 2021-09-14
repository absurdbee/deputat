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
    description = models.CharField(max_length=700, blank=True, verbose_name="Образование")
    list = models.ManyToManyField('lists.AuthorityList', blank=True, related_name='elect_list', verbose_name="Орган гос. власти")
    region = models.ManyToManyField(Region, blank=True, related_name='elect_region', verbose_name="Регионы, за которым закреплен депутат")
    birthday = models.CharField(max_length=100, blank=True, null=True, verbose_name='Дата рождения')
    authorization = models.CharField(max_length=100, blank=True, null=True, verbose_name='Дата наделения полномочиями')
    term_of_office = models.CharField(max_length=100, blank=True, null=True, verbose_name='Срок окончания полномочий')
    election_information = models.CharField(max_length=200, blank=True, verbose_name="Сведения об избрании")
    fraction = models.ForeignKey('lists.Fraction', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Фракции")
    is_active = models.BooleanField(default=True, verbose_name="Активный депутат")
    post_2 = models.CharField(max_length=400, blank=True, null=True, verbose_name='Должность')
    area = models.ManyToManyField('district.District2', blank=True, related_name='elect_area', verbose_name="Районы, за которым закреплен депутат")
    okrug = models.ForeignKey('okrug.Okrug', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Одномандатный избирательный округ")

    vk = models.CharField(max_length=100, blank=True, default="", verbose_name='Ссылка на VK')
    fb = models.CharField(max_length=100, blank=True, default="", verbose_name='Ссылка на Facebook')
    ig = models.CharField(max_length=100, blank=True, default="", verbose_name='Ссылка на Instagram')
    tg = models.CharField(max_length=100, blank=True, default="", verbose_name='Ссылка на Telegram')
    tw = models.CharField(max_length=100, blank=True, default="", verbose_name='Ссылка на Twitter')
    mail = models.CharField(max_length=100, blank=True, default="", verbose_name='Электронная почта')
    phone = models.CharField(max_length=100, blank=True, default="", verbose_name='Телефон')
    address = models.CharField(max_length=100, blank=True, default="", verbose_name='Адрес (приёмная)')

    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    inert = models.PositiveIntegerField(default=0, verbose_name="Кол-во inert")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    old = models.BooleanField(default=False, verbose_name="Старый депутат")
    is_new = models.BooleanField(default=False, verbose_name="Старый депутат")

    class Meta:
        verbose_name = "Чиновник"
        verbose_name_plural = "Чиновники"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def vk_links(self):
        import re
        ids = re.findall(r'https://[\S]+', self.vk)
        text = ""
        for i in ids:
            text += '<a target="_blank" href="' + i + '">' + i + "</a>"
        return text

    def is_have_year(self):
        return len(self.birthday) == 2

    def calculate_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def count_regions(self):
        return self.region.count()
    def get_region_cities(self):
        return self.region.all()[0].get_cities()
    def get_region_districts(self):
        return self.region.all()[0].get_districts()
    def get_cities(self):
        return self.city.all()
    def get_districts(self):
        return self.area.all()

    @classmethod
    def create_elect(cls, creator, name, description, image, list, region, area, birthday, fraction, post_2, vk, tg, tw, ig, fb, mail, phone, address):
        from logs.model.manage_elect_new import ElectManageLog

        name_2 = name.replace("  ", " ").replace("   ", " ").replace("   ", " ").replace("    ", " ")
        elect = cls.objects.create(name=name_2,description=description,post_2=post_2,image=image,birthday=birthday,fraction=fraction,vk=vk, tg=tg, tw=tw, ig=ig, fb=fb, mail=mail, phone=phone, address=phone)
        if region:
            from region.models import Region
            for region_id in region:
                a = Region.objects.get(pk=region_id)
                elect.region.add(a)
        if area:
            from district.models import District2
            for district_id in area:
                a = District2.objects.get(pk=district_id)
                elect.area.add(a)
        if list:
            from lists.models import AuthorityList
            for list_id in list:
                a = AuthorityList.objects.get(pk=list_id)
                elect.list.add(a)
        ElectManageLog.objects.create(item=elect.pk, manager=creator.pk, action_type=ElectManageLog.ITEM_CREATED)
        return list

    def get_region(self):
        from district.models import District2
        if self.region:
            return self.region.all()
        elif self.area:
            return 0
        elif self.okrug:
            return self.okrug.region
        else:
            return []

    def edit_elect(self, name, description, image, list, region, area, birthday, fraction, manager_id, post_2, vk, tg, tw, ig, fb, mail, phone, address):
        from logs.model.manage_elect_new import ElectManageLog

        name_2 = name.replace("  ", " ").replace("   ", " ").replace("   ", " ").replace("    ", " ")
        self.name = name_2
        self.post_2 = post_2
        self.description = description
        self.image = image
        self.birthday = birthday
        self.fraction = fraction

        self.vk = vk
        self.fb = fb
        self.tg = tg
        self.ig = ig
        self.tw = tw
        self.mail = mail
        self.phone = phone
        self.address = address

        self.region.clear()
        self.area.clear()
        self.list.clear()
        self.save()
        if region:
            from region.models import Region
            for region_id in region:
                a = Region.objects.get(pk=region_id)
                self.region.add(a)
        if area:
            from district.models import District2
            for district_id in area:
                a = District2.objects.get(pk=district_id)
                self.area.add(a)
        if list:
            from lists.models import AuthorityList
            for list_id in list:
                a = AuthorityList.objects.get(pk=list_id)
                self.list.add(a)
        ElectManageLog.objects.create(item=self.pk, manager=manager_id, action_type=ElectManageLog.ITEM_EDITED)

    def get_region_image(self):
        return '/static/images/test_2.jpg'

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/static/images/elect_image.png'

    def get_first_list(self):
        try:
            return self.list.all()[0]
        except:
            return ""

    def get_regions(self):
        regions = self.region.all()
        return regions
    def get_districts(self):
        regions = self.area.all()
        return regions

    def get_xxx(self):
        if self.get_regions():
            return self.get_regions()
        elif self.get_districts():
            return self.get_districts()[0].region.name
        elif self.okrug:
            return [self.okrug.region]

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
            #from common.notify.notify import user_notify, user_wall
            #user_notify(user, None, self.pk, "ELE", "u_elec_notify", "LIK", self.pk)
            #user_wall(user, None, self.pk, "ELE", "u_elec_notify", "LIK")
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
            #from common.notify.notify import user_notify, user_wall
            #user_notify(user, None, self.pk, "ELE", "u_elec_notify", "DIS", self.pk)
            #user_wall(user, None, self.pk, "ELE", "u_elec_notify", "DIS")
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
            #from common.notify.notify import user_notify, user_wall
            #user_notify(user, None, self.pk, "ELE", "u_elec_notify", "INE", self.pk)
            #user_wall(user, None, self.pk, "ELE", "u_elec_notify", "INE")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count()),"inert_count": str(self.inerts_count())}),content_type="application/json")

    def is_user_voted(self, user_id):
        from common.model.votes import ElectRating
        return ElectRating.objects.filter(elect_id=self.id, user_id=user_id).exists()

    def get_rating_list(self):
        from common.model.votes import ElectRating
        from django.db.models import Avg
        query = ElectRating.objects.filter(elect_id=self.id)
        vakcine = query.aggregate(Avg('vakcine'))['vakcine__avg']
        pp_825 = query.aggregate(Avg('pp_825'))['pp_825__avg']
        safe_family = query.aggregate(Avg('safe_family'))['safe_family__avg']
        pro_life = query.aggregate(Avg('pro_life'))['pro_life__avg']
        free_vacation = query.aggregate(Avg('free_vacation'))['free_vacation__avg']
        query = [vakcine, pp_825, safe_family, pro_life, free_vacation]
        total = avg = sum(query) / len(query)
        query += [total]
        return query

    def get_vakcine_double(self):
        from common.model.votes import ElectRating
        if not ElectRating.objects.filter(elect_id=self.id).exists():
            return '<td style="background:#FFEB84;text-align: right;"><span>0</span></td>'
        else:
            from django.db.models import Avg
            _double = ElectRating.objects.filter(elect_id=self.id).aggregate(Avg('vakcine'))
            double = round(_double['vakcine__avg'],1)
            if double < -2:
                color = "#FA9D75"
            elif -3 < double < -1:
                color = "#FCB77A"
            elif -2 < double < 0:
                color = "#FDD17F"
            elif -1 < double < 1:
                color = "#FFEB84"
            elif 0 < double < 2:
                color = "#E0E383"
            elif 1 < double < 3:
                color = "#C1DA81"
            else:
                color = "#A2D07F"
        return '<td style="background:' + color + ';text-align: right;"><span>' + str(double) + '</span></td>'
    def get_pp_825_double(self):
        from common.model.votes import ElectRating
        if not ElectRating.objects.filter(elect_id=self.id).exists():
            return '<td style="background:#FFEB84;text-align: right;"><span>0</span></td>'
        else:
            from django.db.models import Avg
            _double = ElectRating.objects.filter(elect_id=self.id).aggregate(Avg('pp_825'))
            double = round(_double['pp_825__avg'],1)
            if double < -2:
                color = "#FA9D75"
            elif -3 < double < -1:
                color = "#FCB77A"
            elif -2 < double < 0:
                color = "#FDD17F"
            elif -1 < double < 1:
                color = "#FFEB84"
            elif 0 < double < 2:
                color = "#E0E383"
            elif 1 < double < 3:
                color = "#C1DA81"
            else:
                color = "#A2D07F"
        return '<td style="background:' + color + ';text-align: right;"><span>' + str(double) + '</span></td>'
    def get_safe_family_double(self):
        from common.model.votes import ElectRating
        if not ElectRating.objects.filter(elect_id=self.id).exists():
            return '<td style="background:#FFEB84;text-align: right;"><span>0</span></td>'
        else:
            from django.db.models import Avg
            _double = ElectRating.objects.filter(elect_id=self.id).aggregate(Avg('safe_family'))
            double = round(_double['safe_family__avg'],1)
            if double < -2:
                color = "#FA9D75"
            elif -3 < double < -1:
                color = "#FCB77A"
            elif -2 < double < 0:
                color = "#FDD17F"
            elif -1 < double < 1:
                color = "#FFEB84"
            elif 0 < double < 2:
                color = "#E0E383"
            elif 1 < double < 3:
                color = "#C1DA81"
            else:
                color = "#A2D07F"
        return '<td style="background:' + color + ';text-align: right;"><span>' + str(double) + '</span></td>'
    def get_pro_life_double(self):
        from common.model.votes import ElectRating
        if not ElectRating.objects.filter(elect_id=self.id).exists():
            return '<td style="background:#FFEB84;text-align: right;"><span>0</span></td>'
        else:
            from django.db.models import Avg
            _double = ElectRating.objects.filter(elect_id=self.id).aggregate(Avg('pro_life'))
            double = round(_double['pro_life__avg'],1)
            if double < -2:
                color = "#FA9D75"
            elif -3 < double < -1:
                color = "#FCB77A"
            elif -2 < double < 0:
                color = "#FDD17F"
            elif -1 < double < 1:
                color = "#FFEB84"
            elif 0 < double < 2:
                color = "#E0E383"
            elif 1 < double < 3:
                color = "#C1DA81"
            else:
                color = "#A2D07F"
        return '<td style="background:' + color + ';text-align: right;"><span>' + str(double) + '</span></td>'
    def get_free_vacation_double(self):
        from common.model.votes import ElectRating
        if not ElectRating.objects.filter(elect_id=self.id).exists():
            return '<td style="background:#FFEB84;text-align: right;"><span>0</span></td>'
        else:
            from django.db.models import Avg
            _double = ElectRating.objects.filter(elect_id=self.id).aggregate(Avg('free_vacation'))
            double = round(_double['free_vacation__avg'],1)
            if double < -2:
                color = "#FA9D75"
            elif -3 < double < -1:
                color = "#FCB77A"
            elif -2 < double < 0:
                color = "#FDD17F"
            elif -1 < double < 1:
                color = "#FFEB84"
            elif 0 < double < 2:
                color = "#E0E383"
            elif 1 < double < 3:
                color = "#C1DA81"
            else:
                color = "#A2D07F"
        return '<td style="background:' + color + ';text-align: right;"><span>' + str(double) + '</span></td>'

    def get_total_rating_double(self):
        from common.model.votes import ElectRating
        if not ElectRating.objects.filter(elect_id=self.id).exists():
            return '<td style="background:#FFEB84;text-align: right;"><span>0</span></td>'
        else:
            from django.db.models import Avg
            query = ElectRating.objects.filter(elect_id=self.id)
            vakcine = query.aggregate(Avg('vakcine'))['vakcine__avg']
            pp_825 = query.aggregate(Avg('pp_825'))['pp_825__avg']
            safe_family = query.aggregate(Avg('safe_family'))['safe_family__avg']
            pro_life = query.aggregate(Avg('pro_life'))['pro_life__avg']
            free_vacation = query.aggregate(Avg('free_vacation'))['free_vacation__avg']
            list = [vakcine, pp_825, safe_family, pro_life, free_vacation]
            avg = sum(list) / len(list)
            double = round(avg,1)
            if double < -2:
                color = "#FA9D75"
            elif -3 < double < -1:
                color = "#FCB77A"
            elif -2 < double < 0:
                color = "#FDD17F"
            elif -1 < double < 1:
                color = "#FFEB84"
            elif 0 < double < 2:
                color = "#E0E383"
            elif 1 < double < 3:
                color = "#C1DA81"
            else:
                color = "#A2D07F"
            return '<td style="background:' + color + ';text-align: right;"><span>' + str(double) + '</span></td>'
    def get_manager_total_rating_double(self):
        from common.model.votes import ElectRating
        if not ElectRating.objects.filter(elect_id=self.id).exists():
            return '<td style="background:#FFEB84;text-align: center;"><span>0</span></td>'
        else:
            from django.db.models import Avg
            query = ElectRating.objects.filter(elect_id=self.id)
            vakcine = query.aggregate(Avg('vakcine'))['vakcine__avg']
            pp_825 = query.aggregate(Avg('pp_825'))['pp_825__avg']
            safe_family = query.aggregate(Avg('safe_family'))['safe_family__avg']
            pro_life = query.aggregate(Avg('pro_life'))['pro_life__avg']
            free_vacation = query.aggregate(Avg('free_vacation'))['free_vacation__avg']
            list = [vakcine, pp_825, safe_family, pro_life, free_vacation]
            avg = sum(list) / len(list)
            double = round(avg,1)
            if avg < -2:
                color = "#FA9D75"
            elif -3 < double < -1:
                color = "#FCB77A"
            elif -2 < double < 0:
                color = "#FDD17F"
            elif -1 < double < 1:
                color = "#FFEB84"
            elif 0 < double < 2:
                color = "#E0E383"
            elif 1 < double < 3:
                color = "#C1DA81"
            else:
                color = "#A2D07F"
            return '<td style="background:' + color + ';text-align: center;"><span>' + str(double) + '</span></td>'

    def get_total_rating_icon(self):
        from common.model.votes import ElectRating
        if not ElectRating.objects.filter(elect_id=self.id).exists():
            return '<span class="elect_rating_icon"><span class="integer">0</span><svg fill="#FFEB84" enable-background="new 0 0 20 20" width="24" height="24" viewBox="0 0 24 24"><g><rect x="0"></rect><polygon points="14.43,10 12,2 9.57,10 2,10 8.18,14.41 5.83,22 12,17.31 18.18,22 15.83,14.41 22,10"></polygon></g></svg></span>'
        else:
            from django.db.models import Avg

            query = ElectRating.objects.filter(elect_id=self.id)
            vakcine = query.aggregate(Avg('vakcine'))['vakcine__avg']
            pp_825 = query.aggregate(Avg('pp_825'))['pp_825__avg']
            safe_family = query.aggregate(Avg('safe_family'))['safe_family__avg']
            pro_life = query.aggregate(Avg('pro_life'))['pro_life__avg']
            free_vacation = query.aggregate(Avg('free_vacation'))['free_vacation__avg']
            list = [vakcine, pp_825, safe_family, pro_life, free_vacation]
            avg = sum(list) / len(list)
            double = round(avg,1)
            if double < -2:
                color = "#FA9D75"
            elif -3 < double < -1:
                color = "#FCB77A"
            elif -2 < double < 0:
                color = "#FDD17F"
            elif -1 < double < 1:
                color = "#FFEB84"
            elif 0 < double < 2:
                color = "#E0E383"
            elif 1 < double < 3:
                color = "#C1DA81"
            else:
                color = "#A2D07F"
            return '<span class="elect_rating_icon"><span class="integer">' + str(double) + '</span><svg fill="' + color + '" enable-background="new 0 0 20 20" width="24" height="24" viewBox="0 0 24 24"><g><rect x="0"></rect><polygon points="14.43,10 12,2 9.57,10 2,10 8.18,14.41 5.83,22 12,17.31 18.18,22 15.83,14.41 22,10"></polygon></g></svg></span>'


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


class ElectStat(models.Model):
    GGOD = 1
    NORMAL = 0
    BAD = -1

    LEVEL = (
        (GGOD, 'Молодец'),
        (NORMAL, 'Нормальный'),
        (BAD, 'Не молодец'),
    )
    elect = models.OneToOneField(Elect, on_delete=models.CASCADE, related_name='elect_stat', verbose_name="Пользователь")
    lgbt = models.SmallIntegerField(choices=LEVEL, default=NORMAL, verbose_name="Отношение к ЛГБТ")
    yuvenal = models.SmallIntegerField(choices=LEVEL, default=NORMAL, verbose_name="Отношение к ювеналке")
    med_fascism = models.SmallIntegerField(choices=LEVEL, default=NORMAL, verbose_name="Отношение к мед. фашизму")
    abort = models.SmallIntegerField(choices=LEVEL, default=NORMAL, verbose_name="Отношение к абортам")
    educations = models.SmallIntegerField(choices=LEVEL, default=NORMAL, verbose_name="Отношение к образованию")

    express_loans = models.SmallIntegerField(choices=LEVEL, default=NORMAL, verbose_name="Отношение к экспресс-судам")
    sbn = models.SmallIntegerField(choices=LEVEL, default=NORMAL, verbose_name="Отношение к СБН")
    surrogat_mom = models.SmallIntegerField(choices=LEVEL, default=NORMAL, verbose_name="Отношение к суррогатному материнству")
