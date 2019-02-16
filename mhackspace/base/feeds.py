from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from mhackspace.feeds.models import Article


class MediaRssFeed(Rss201rev2Feed):
    """
    Implement thumbnails which adhere to Yahoo Media RSS (mrss) feed.

    @see http://djangosnippets.org/snippets/1648/
    """

    def rss_attributes(self):
        attrs = super(MediaRssFeed, self).rss_attributes()
        attrs["xmlns:dc"] = "http://purl.org/dc/elements/1.1/"
        attrs["xmlns:media"] = "http://search.yahoo.com/mrss/"
        return attrs

    def add_item_elements(self, handler, item):
        super(MediaRssFeed, self).add_item_elements(handler, item)

        if item.get("thumbnail_url") is None:
            return

        thumbnail = {"url": item["thumbnail_url"]}

        if "thumbnail_width" in item:
            thumbnail["width"] = str(item["thumbnail_width"])

        if "thumbnail_height" in item:
            thumbnail["height"] = str(item["thumbnail_height"])

        handler.addQuickElement(u"media:thumbnail", "", thumbnail)


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
