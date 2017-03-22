from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from mhackspace.blog.models import Category, Post

class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(active=True, members_only=False, published_date__lte=timezone.now())

    def lastmod(self, obj):
        return obj.updated_date

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Category.objects.all()
