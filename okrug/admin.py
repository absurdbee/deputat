from django.contrib import admin
from okrug.models import Okrug


class OkrugAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'order', 'slug']
    list_filter = ['region']
    search_fields = ['name']

    class Meta:
            model = Okrug

admin.site.register(Okrug, OkrugAdmin)
