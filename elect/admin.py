from django.contrib import admin
from elect.models import Elect, LinkElect


class ElectAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    list_filter = ['name',]
    search_fields = ['name',]
    class Meta:
            model = Elect

class LinkElectAdmin(admin.ModelAdmin):
    list_display = ['title','elect']
    list_filter = ['elect']
    search_fields = ['title','elect',]
    class Meta:
            model = LinkElect

admin.site.register(Elect, ElectAdmin)
admin.site.register(LinkElect, LinkElectAdmin)
