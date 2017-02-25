from rest_framework import serializers

from mhackspace.feeds.models import Feed, Article


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('home_url', 'feed_url', 'title', 'author', 'tags', 'image')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('url', 'feed', 'original_image', 'image', 'description', 'date')
