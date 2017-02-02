from django.contrib.syndication.views import Feed
from django.urls import reverse
from mhackspace.feeds.models import Article

class LatestEntriesFeed(Feed):
    title = "Maidstone hackspace site news"
    link = "/latest/"
    description = "Latest creations from our users."

    def items(self):
        return Article.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.url 
