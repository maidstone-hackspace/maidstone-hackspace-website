from django.contrib.sitemaps import Sitemap
from mhackspace.blog.models import Category, Post

class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(active=True, members_only=False)

    def lastmod(self, obj):
        return obj.published_date

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Category.objects.all()
