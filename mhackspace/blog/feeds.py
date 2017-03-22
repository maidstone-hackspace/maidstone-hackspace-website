from django.contrib.syndication.views import Feed
from django.utils import timezone

from mhackspace.blog.models import Category, Post


class BlogFeed(Feed):
    title = "Maidstone Hackspace Blog"
    link = "/blog/"
    description = "The latest blog posts and news from the Maidstone Hackspace site"

    def items(self, category):
        return Post.objects.select_related('author').filter(active=True, members_only=False, published_date__lte=timezone.now())[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_author_name(self, item):
        return item.author.name

    def item_author_email(self, item):
        if item.author.public:
            return item.author.email

    def item_categories(self, item):
        return item.categories.all()

    def item_pubdate(self, item):
        return item.published_date

    def item_updateddate(self, item):
        return item.updated_date


class BlogCategoryFeed(BlogFeed):
    def get_object(self, request, category):
        return Category.objects.filter(slug=category).first()

    def items(self, category):
        return Post.objects.select_related('author').filter(active=True, members_only=False, categories=category, published_date__lte=timezone.now())[:20]

    def title(self, category):
        return "Maidstone Hackspace Blog: %s" % category.name

    def description(self, category):
        return category.description
