from django.contrib import admin
from video.models import VideoCategory, VideoList, Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'community', 'creator']
    search_fields = ('title',)

admin.site.register(VideoList)
admin.site.register(VideoCategory)
admin.site.register(Video, VideoAdmin)
