from autofixture import AutoFixture
from autofixture.generators import ImageGenerator
from django.core.management.base import BaseCommand
from mhackspace.base.models import BannerImages
from mhackspace.feeds.models import Article, Feed
from mhackspace.users.models import User

class ImageFixture(AutoFixture):
    class Values:
        scaled_image = ImageGenerator(width=800, height=300, sizes=((1280, 300),))

class Command(BaseCommand):
    help = 'Build test data for development environment'

    def handle(self, *args, **options):
        users = AutoFixture(User)
        users.create(10)

        feed = AutoFixture(Feed)
        feed.create(10)

        feeds = AutoFixture(Article)
        feeds.create(10)

        banners = ImageFixture(BannerImages)
        banners.create(10)
        self.stdout.write(
            self.style.SUCCESS(
                'Finished creating test data'))