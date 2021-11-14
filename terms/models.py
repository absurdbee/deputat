from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Terms(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    content = RichTextUploadingField(config_name='default',)
