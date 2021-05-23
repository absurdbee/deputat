from django.contrib import admin
from users.models import User
from users.model.profile import *
from users.model.settings import *


class UserNotificationsInline(admin.TabularInline):
    model = UserNotifications
class UserPrivateInline(admin.TabularInline):
    model = UserPrivate
class UserInfoInline(admin.TabularInline):
    model = UserInfo

class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserNotificationsInline,
        UserPrivateInline,
        UserInfoInline,
        ]
    list_display = ['pk', 'phone']
    search_fields = ('last_name','first_name')
    model = User


admin.site.register(UserInfo)
admin.site.register(User, UserAdmin)
admin.site.register(UserLocation)
admin.site.register(UserTransaction)
admin.site.register(UserCheck)
