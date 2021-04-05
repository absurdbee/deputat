from django.contrib import admin
from music.models import *


class MusicAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['tag', 'genre']
    class Meta:
            model = Music


admin.site.register(Music, MusicAdmin)
admin.site.register(SoundList)
