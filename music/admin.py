from django.contrib import admin
from music.models import *


class MusicAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    class Meta:
            model = Music

admin.site.register(Music, MusicAdmin)
admin.site.register(SoundList)
