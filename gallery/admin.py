from django.contrib import admin
from gallery.models import Album, Photo


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'created']
    list_filter = ['creator', ]
    class Meta:
        model = Album

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['creator', 'created']
    list_filter = ['creator', ]

    class Meta:
            model = Photo

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
