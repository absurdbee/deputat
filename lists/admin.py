from django.contrib import admin
from lists.models import ElectList, ElectNewsCategory, BlogCategory, Region


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

class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_filter = ['name']
    search_fields = ('name',)
    class Meta:
        model = Region


admin.site.register(ElectList, ElectListAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Region, RegionAdmin)
