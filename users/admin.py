from django.contrib import admin
from users.models import User
from users.model.profile import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'phone']
    search_fields = ('last_name','first_name')
    model = User


admin.site.register(User)
admin.site.register(UserLocation)
admin.site.register(UserInfo)
admin.site.register(UserTransaction)
admin.site.register(UserCheck)
