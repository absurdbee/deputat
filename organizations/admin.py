from django.contrib import admin
from organizations.models import Organization


class OrganizationAdmin(admin.ModelAdmin):

    list_display = ['name','order','type']
    list_filter = ['type']
    search_fields = ['name']
    class Meta:
            model = Organization

admin.site.register(Organization,OrganizationAdmin)
