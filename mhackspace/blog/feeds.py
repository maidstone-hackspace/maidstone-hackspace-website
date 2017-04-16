from django.contrib.syndication.views import Feed, add_domain
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone

from mhackspace.base.feeds import MediaRssFeed
from mhackspace.blog.models import Category, Post


class BlogFeed(Feed):
    title = "Maidstone Hackspace Blog"
    link = "/blog/"
    feed_type = MediaRssFeed
    description = "The latest blog posts and news from the Maidstone Hackspace site"

    def get_feed(self, obj, request):
        self.current_site = get_current_site(request)
        return super(BlogFeed, self).get_feed(obj, request)

    def items(self, category):
        return Post.objects.select_related('author').filter(
            active=True,
            members_only=False,
            published_date__lte=timezone.now())[:20]

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        return post.description

    def item_author_name(self, post):
        return post.author.name

    def item_author_email(self, post):
        if post.author.public:
            return post.author.email

    def item_categories(self, post):
        return post.categories.all()

    def item_pubdate(self, post):
        return post.published_date

    def item_updateddate(self, post):
        return post.updated_date

    def item_extra_kwargs(self, post):
        return {
            'thumbnail_url': add_domain(
                domain=self.current_site.domain,
                url=post.image.full.url,
                secure=True),
            'thumbnail_width': post.image.full.width,
            'thumbnail_height': post.image.full.height,
        }


class BlogCategoryFeed(BlogFeed):
    def get_object(self, request, category):
        return Category.objects.filter(slug=category).first()

    def items(self, category):
        return Post.objects.select_related('author').filter(
            active=True,
            members_only=False,
            categories=category,
            published_date__lte=timezone.now())[:20]

    def title(self, category):
        return "Maidstone Hackspace Blog: %s" % category.name

    def description(self, category):
        return category.description
