from django.contrib import admin
from .models import News, Comments

class CommentInline(admin.TabularInline):
    model = Comments
    extra = 5


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'has_comments')
    inlines = [CommentInline]

admin.site.register(News, NewsAdmin)
admin.site.register(Comments)
