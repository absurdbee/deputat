from django.contrib import admin
from lists.models import AuthorityList, ElectNewsCategory, BlogCategory, Region, Fraction


class AuthorityListAdmin(admin.ModelAdmin):
    list_display = ['name','slug','order']
    list_filter = ['name']
    search_fields = ('name',)
    class Meta:
        model = AuthorityList

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

class FractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_filter = ['name']
    search_fields = ('name',)
    class Meta:
        model = Fraction

admin.site.register(ElectList, ElectListAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Fraction, FractionAdmin)
