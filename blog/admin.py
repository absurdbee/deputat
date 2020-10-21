from django.contrib import admin
from blog.models import Blog, BlogComment, ElectNew


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created']
    list_filter = ['created', 'category']
    search_fields = ['title', 'description', 'created']
    exclude = ('count',)

    class Meta:
            model = Blog

    def get_form(self, request, *args, **kwargs):
        form = super(BlogAdmin, self).get_form(request, *args, **kwargs)
        form.base_fields['creator'].initial = request.user
        return form

class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['text','commenter','created']
    list_filter = ['created']
    search_fields = ['created','text','commenter']

    class Meta:
            model = BlogComment

class ElectNewAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created', 'elect', 'category']
    list_filter = ['created', 'category']
    search_fields = ['title', 'description', 'created']
    exclude = ('count',)

    class Meta:
            model = ElectNew

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
