from django.contrib import admin
from quan.models import *

class FilesInline(admin.TabularInline):
    model = SupportFile

class SupportAdmin(admin.ModelAdmin):
    inlines = [
        SupportFile,
    ]
    list_display = ['creator', 'type', 'description']
    search_fields = ('description')
    model = Support


admin.site.register(Support, SupportAdmin)
