from django.contrib import admin
from elect.models import *


class LinkElectInline(admin.TabularInline):
    model = LinkElect
class EducationElectInline(admin.TabularInline):
    model = EducationElect


class ElectAdmin(admin.ModelAdmin):
    inlines = [
        LinkElectInline,
        EducationElectInline,
    ]
    list_display = ['name', ]
    list_filter = ['list',]
    search_fields = ['name',]
    class Meta:
            model = Elect


admin.site.register(Elect, ElectAdmin)
admin.site.register(SubscribeElect)
