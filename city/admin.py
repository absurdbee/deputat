from django.contrib import admin
from city.models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'link', 'slug']
    list_filter = ['region']
    search_fields = ['name']

    class Meta:
            model = City

admin.site.register(City, CityAdmin)
