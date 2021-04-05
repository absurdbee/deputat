from django.contrib import admin
from video.models import VideoCategory, VideoAlbum, Video



admin.site.register(VideoAlbum)
admin.site.register(VideoCategory)
admin.site.register(Video)
