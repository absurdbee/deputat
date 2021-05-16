from django.contrib import admin
from video.models import VideoCategory, VideoList, Video



admin.site.register(VideoList)
admin.site.register(VideoCategory)
admin.site.register(Video)
