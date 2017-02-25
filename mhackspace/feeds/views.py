from rest_framework import filters, viewsets
from mhackspace.feeds.models import Feed, Article
from mhackspace.feeds.serializers import FeedSerializer, ArticleSerializer


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.filter(enabled=True)
    serializer_class = FeedSerializer
    search_fields = ('home_url', 'feed_url', 'title', 'author__name', 'tags', 'image')
    ordering_fields = ('home_url', 'feed_url', 'title', 'author', 'tags', 'image')
    filter_fields = ('home_url', 'feed_url', 'title', 'author', 'tags', 'image')


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(displayed=True)
    serializer_class = ArticleSerializer
    search_fields = ('url', 'feed__title', 'original_image', 'description', 'date')
    ordering_fields = ('url', 'feed', 'date')
    filter_fields = ('url', 'feed', 'date')
