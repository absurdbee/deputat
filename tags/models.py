from django.db import models
from blog.models import Blog, ElectNew


class ManagerTag(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    parent = models.ForeignKey("self", blank=True, null=True, related_name='+', on_delete=models.CASCADE, verbose_name="Родитель")

    class Meta:
        verbose_name = "Наш тег"
        verbose_name_plural = "Наши теги"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_blog_ids(self):
        blogs = self.blog.values("pk")
        return [i['pk'] for i in blogs]

    def get_blog_ids(self):
        blogs = self.blog.values("pk")
        return [i['pk'] for i in blogs]

    def get_new_ids(self):
        news = self.new.values("pk")
        return [i['pk'] for i in news]

    @classmethod
    def remove_blog(cls, _blog):
        cls.blog.remove(self)
