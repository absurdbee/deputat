from django.contrib import admin
from region.models import Region


class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    search_fields = ['name']
    class Meta:
            model = Region

admin.site.register(Region, RegionAdmin)
