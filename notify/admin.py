from django.contrib import admin
from notify.models import *


class NotifyAdmin(admin.ModelAdmin):
    list_display = ['creator','recipient','created']
    list_filter = ['created']
    class Meta:
        model = Notify

class WallAdmin(admin.ModelAdmin):
    list_display = ['creator', 'created']
    list_filter = ['created']
    class Meta:
        model = Wall


admin.site.register(Notify, NotifyAdmin)
admin.site.register(Wall, WallAdmin)

admin.site.register(UserNewsNotify)
admin.site.register(UserProfileNotify)
