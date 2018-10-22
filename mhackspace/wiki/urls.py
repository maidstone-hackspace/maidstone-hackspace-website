from wiki.urls import WikiURLPatterns
from mhackspace.wiki.views import WikiArticleView


class CustomWikiUrlPatterns(WikiURLPatterns):
    article_view_class = WikiArticleView
