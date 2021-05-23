from django.contrib import admin
from blog.models import *


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created']
    list_filter = ['created']
    search_fields = ['title', 'description', 'created']
    exclude = ('count',)

    class Meta:
            model = Blog

    def get_form(self, request, *args, **kwargs):
        form = super(BlogAdmin, self).get_form(request, *args, **kwargs)
        form.base_fields['creator'].initial = request.user
        return form

admin.site.register(Blog, BlogAdmin)
admin.site.register(ElectNew)
