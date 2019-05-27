from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.urls import reverse

from mhackspace.base.tasks import update_homepage_feeds
from mhackspace.feeds.models import Feed, Article
from mhackspace.feeds.helper import import_feeds


@admin.register(Feed)
class FeedAdmin(ModelAdmin):
    list_display = ("title", "home_url", "author", "tags", "enabled")
    list_filter = ("enabled",)


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    date_hierarchy = "date"
    list_display = ("title", "url", "feed", "date", "displayed")
    list_filter = ("displayed", "feed", "feed__author")
    readonly_fields = ("original_image",)
    ordering = ("-date",)

    def get_urls(self):
        urls = super(ArticleAdmin, self).get_urls()
        my_urls = [
            url(r"^import/$", self.admin_site.admin_view(self.import_articles))
        ]
        return my_urls + urls

    def import_articles(self, request):
        update_homepage_feeds()
        self.message_user(
            request,
            "Importing articles in background refresh in a few minutes",
        )
        return HttpResponseRedirect(reverse("admin:feeds_article_changelist"))


admin.site.site_title = "Maidstone Hackspace Admin Area"
admin.site.site_header = "Maidstone Hackspace Admin Area"
admin.site.index_title = "Maidstone Admin Home"
