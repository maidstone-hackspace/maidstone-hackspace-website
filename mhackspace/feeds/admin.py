from django.contrib import admin
from django.contrib.admin import AdminSite, TabularInline, ModelAdmin
from mhackspace.feeds.models import Feed


@admin.register(Feed)
class FeedAdmin(ModelAdmin):
    list_display = ('url', 'author', 'tags', 'enabled')

admin.site.site_title = 'Maidstone hackspace Admin Area'
admin.site.site_header = 'Maidstone hackspace Admin Area'
admin.site.index_title = 'Maidstone Admin Home'
