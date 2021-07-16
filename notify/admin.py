from django.contrib import admin
from notify.models import *


class WallAdmin(admin.ModelAdmin):
    list_display = ['creator','verb','type','object_id']
    search_fields = ['title']
    class Meta:
            model = Wall

class NotifyAdmin(admin.ModelAdmin):
    list_display = ['creator','recipient','verb','type','object_id']
    search_fields = ['title']
    class Meta:
            model = Notify

admin.site.register(Notify, NotifyAdmin)
admin.site.register(Wall, WallAdmin)

admin.site.register(UserNewsNotify)
admin.site.register(UserProfileNotify)
