from django.db import models
from django.conf import settings


"""
    Группируем "другие" таблицы здесь:
    1. Телефонные коды, присылаемые пользователям при подтверждении телефона
"""

class PhoneCodes(models.Model):
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    code = models.PositiveSmallIntegerField(default=0, verbose_name="Код")
    id = models.BigAutoField(primary_key=True)

class RecoveryPhoneCodes(models.Model):
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    code = models.PositiveSmallIntegerField(default=0, verbose_name="Код")
    id = models.BigAutoField(primary_key=True)


class StickerCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='+', verbose_name="Пользователь")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = 'Категория стикеров'
        verbose_name_plural = 'Категории стикеров'

    def __str__(self):
        return self.name

    def get_items(self):
        return Stickers.objects.filter(category_id=self.pk)

class Stickers(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    category = models.ForeignKey(StickerCategory, on_delete=models.CASCADE, related_name='+', verbose_name="Категория")
    image = models.FileField(upload_to="stickers/")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

    class Meta:
        verbose_name = 'Стикер'
        verbose_name_plural = 'Стикеры'

    def __str__(self):
        return self.name

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

class SmileCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
    classic = models.BooleanField(default=True, verbose_name="Классические")
    gif = models.BooleanField(default=False, verbose_name="Анимированные")

    class Meta:
        verbose_name = 'Категория смайликов'
        verbose_name_plural = 'Категории смайликов'

    def __str__(self):
        return self.name

    def get_items(self):
        return Smiles.objects.filter(category_id=self.pk)


class Smiles(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(SmileCategory, on_delete=models.CASCADE, related_name='+', verbose_name="Категория")
    image = models.FileField(upload_to="smiles/")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

    class Meta:
        verbose_name = 'Смайл'
        verbose_name_plural = 'Смайлы'

    def __str__(self):
        return self.name

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

class UserPopulateSmiles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', verbose_name="Пользователь")
    smile = models.ForeignKey(Smiles, on_delete=models.CASCADE, related_name='smile', verbose_name="Смайл")
    count = models.PositiveIntegerField(default=1, verbose_name="Количество использований пользователем")

    class Meta:
        verbose_name = 'Популярность смайликов'
        verbose_name_plural = 'Популярность смайликов'
        ordering = ['-count']

    def __str__(self):
        return self.user.get_full_name()

    def get_plus_or_create(user_pk, smile_pk):
        if UserPopulateSmiles.objects.filter(user_id=user_pk, smile_id=smile_pk).exists():
            md = UserPopulateSmiles.objects.get(user_id=user_pk, smile_id=smile_pk)
            md.count += 1
            md.save(update_fields=["count"])
        else:
            UserPopulateSmiles.objects.create(user_id=user_pk, smile_id=smile_pk)


class UserPopulateStickers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', verbose_name="Пользователь")
    sticker = models.ForeignKey(Stickers, on_delete=models.CASCADE, related_name='sticker', verbose_name="Стикер")
    count = models.PositiveIntegerField(default=1, verbose_name="Количество использований пользователем")

    class Meta:
        verbose_name = 'Популярность стикеров'
        verbose_name_plural = 'Популярность стикеров'
        ordering = ['-count']

    def __str__(self):
        return self.user.get_full_name()

    def get_plus_or_create(user_pk, sticker_pk):
        if UserPopulateStickers.objects.filter(user_id=user_pk, sticker_id=sticker_pk).exists():
            md = UserPopulateStickers.objects.get(user_id=user_pk, sticker_id=sticker_pk)
            md.count += 1
            md.save(update_fields=["count"])
        else:
            UserPopulateStickers.objects.create(user_id=user_pk, sticker_id=sticker_pk)
