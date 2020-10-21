from django.contrib import admin
from lists.models import ElectList, ElectNewsCategory, BlogCategory


class ElectListAdmin(admin.ModelAdmin):
    list_display = ['name','slug','order']
    list_filter = ['name']
    search_fields = ('name',)
    class Meta:
        model = ElectList

class ElectNewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','order']
    list_filter = ['name']
    search_fields = ('name',)
    class Meta:
        model = ElectNewsCategory

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','order']
    list_filter = ['name']
    search_fields = ('name',)
    class Meta:
        model = BlogCategory


admin.site.register(ElectList, ElectListAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
