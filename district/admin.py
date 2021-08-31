from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from district.models import District


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'order', 'slug']
    list_filter = ['region']
    search_fields = ['name']

    class Meta:
            model = District

admin.site.register(District, DistrictAdmin)
>>>>>>> fb709b6ca3f6a9ce96c10988017008dd0023af4d
