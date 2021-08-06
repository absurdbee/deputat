from django.contrib import admin
from bars.models import BarsMovie, BarsComment, BarsCategory

class BarsMovieAdmin(admin.ModelAdmin):

    list_display = ['title','description','posted']
    list_filter = ['posted']
    search_fields = ['title','description','posted']
    class Meta:
            model = BarsMovie

class BarsCommentAdmin(admin.ModelAdmin):

    list_display = ['article_id','author_id','content']
    list_filter = ['posted']
    search_fields = ['article_id','author_id','content']
    class Meta:
            model = BarsComment

class BarsCategoryAdmin(admin.ModelAdmin):

    list_display = ['name','order']
    search_fields = ['name']
    class Meta:
            model = BarsCategory


admin.site.register(BarsMovie,BarsMovieAdmin)
admin.site.register(BarsComment,BarsCommentAdmin)
admin.site.register(BarsCategory,BarsCategoryAdmin)
