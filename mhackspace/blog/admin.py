from django.contrib import admin
from django.db import models
from django.contrib.admin import ModelAdmin
from markdownx.widgets import AdminMarkdownxWidget

from mhackspace.blog.models import Post, Category

@admin.register(Post)
class PostAdmin(ModelAdmin):
    date_hierarchy = 'published_date'
    list_display = ('title', 'slug', 'author','active', 'members_only', 'published_date', 'updated_date')
    list_filter = ('author', 'categories', 'members_only')
    search_fields = ('title', 'author__name', 'author__id', 'published_date', 'updated_date')
    readonly_fields = ('published_date',)
    filter_horizontal = ('categories',)
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}
