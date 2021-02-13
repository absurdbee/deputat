from django.contrib import admin
from users.models import User
from users.model.profile import UserLocation


class UserLocationInline(admin.TabularInline):
    model = UserLocation

class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'phone']
    inlines = [
        UserLocationInline,
    ]
    search_fields = ('last_name','first_name')


admin.site.register(User)
