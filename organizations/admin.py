from django.contrib import admin
from organizations.models import Organizations


class OrganizationsAdmin(admin.ModelAdmin):

    list_display = ['name','order','type']
    list_filter = ['type']
    search_fields = ['name']
    class Meta:
            model = Organizations

admin.site.register(Organizations,OrganizationsAdmin)
