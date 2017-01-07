from django.contrib import admin
from django.contrib.admin import ModelAdmin
from mhackspace.feeds.models import Feed


@admin.register(Feed)
class FeedAdmin(ModelAdmin):
    list_display = ('url', 'author', 'tags', 'enabled')
    list_filter = ('enabled', )

admin.site.site_title = 'Maidstone Hackspace Admin Area'
admin.site.site_header = 'Maidstone Hackspace Admin Area'
admin.site.index_title = 'Maidstone Admin Home'
