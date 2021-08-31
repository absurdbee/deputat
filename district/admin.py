from django.contrib import admin
from district.models import District


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'order', 'slug']
    list_filter = ['region']
    search_fields = ['name']

    class Meta:
            model = District

admin.site.register(District, DistrictAdmin)
