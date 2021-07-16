from django.contrib import admin
from notify.models import *


class WallAdmin(admin.ModelAdmin):
    list_display = ['creator','verb','type','object_id']
    search_fields = ['title']
    class Meta:
            model = Wall


admin.site.register(Notify)
admin.site.register(Wall, WallAdmin)

admin.site.register(UserNewsNotify)
admin.site.register(UserProfileNotify)
