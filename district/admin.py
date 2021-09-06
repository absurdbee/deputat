from django.contrib import admin
from district.models import District2


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'order', 'slug']
    list_filter = ['region']
    search_fields = ['name']

    class Meta:
            model = District2

admin.site.register(District2, DistrictAdmin)
admin.site.register(District2, DistrictAdmin)
