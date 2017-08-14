import random
from autofixture import AutoFixture
from autofixture.generators import ImageGenerator
from django.core.management.base import BaseCommand
from django.core.management import call_command
from mhackspace.base.models import BannerImage
from mhackspace.feeds.models import Article, Feed
from mhackspace.users.models import User
from mhackspace.blog.models import Category, Post


class ImageFixture(AutoFixture):
    class Values:
        scaled_image = ImageGenerator(width=800, height=300, sizes=((1280, 300),))


class Command(BaseCommand):
    help = 'Build test data for development environment'

    def handle(self, *args, **options):
        feeds = AutoFixture(Article)
        feeds.create(10)
        feed = AutoFixture(Feed)
        feed.create(10)

        post = AutoFixture(Post)
        post.create(10)

        categorys = AutoFixture(Category)
        categorys.create(10)

        # load known data
        call_command('loaddata', 'mhackspace/users/fixtures/groups.json', verbose=0)

        # random data
        users = AutoFixture(User, field_values={
            'title': random.choicee(('Mr', 'Mrs', 'Emperor', 'Captain'))
        })
        users.create(10)

        banners = ImageFixture(BannerImage)
        banners.create(10)
        self.stdout.write(
            self.style.SUCCESS(
                'Finished creating test data'))
