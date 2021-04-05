from django.contrib import admin
from .models import *


class MusicAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['tag', 'genre']
    class Meta:
            model = Music

class SoundTagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol']
    search_fields = ['name']
    list_filter = ['symbol']
    class Meta:
            model = SoundTags


admin.site.register(Music, MusicAdmin)
admin.site.register(SoundList)
