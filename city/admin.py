from django.contrib import admin
from city.models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'pk']
    search_fields = ['title']
    class Meta:
            model = City

admin.site.register(City, CityAdmin)
