from django.contrib import admin
from elect.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ElectResource(resources.ModelResource):

    class Meta:
        model = Elect
        fields = ('name', 'description', 'list__name', 'region__name', 'birthday', 'authorization', 'fraction__name', 'post_2', 'area__name')
        export_order = ('name', 'list__name', 'region__name', 'area__name', 'fraction__name', 'description', 'birthday', 'authorization', 'post_2')

class LinkElectInline(admin.TabularInline):
    model = LinkElect
class EducationElectInline(admin.TabularInline):
    model = EducationElect


class ElectAdmin(ImportExportModelAdmin):
    inlines = [
        LinkElectInline,
        EducationElectInline,
    ]
    list_display = ['name', ]
    list_filter = ['list',]
    search_fields = ['name',]
    resource_class = ElectResource

    class Meta:
            model = Elect


admin.site.register(Elect, ElectAdmin)
admin.site.register(SubscribeElect)
