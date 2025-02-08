from django.contrib import admin
from .models import Author, Post
from django_summernote.admin import SummernoteModelAdmin

# Admin for Author Model
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email'),
        }),
        ('Additional Details', {
            'fields': ('bio', 'profile_picture'),
            'classes': ('collapse',),
        }),
    )


# Admin for Post Model with Summernote Integration
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'date_updated')
    list_filter = ('author', 'date_updated')
    search_fields = ('title', 'description', 'body')
    prepopulated_fields = {'slug': ('title',)}

    summernote_fields = ('body',)

# Register Models
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)