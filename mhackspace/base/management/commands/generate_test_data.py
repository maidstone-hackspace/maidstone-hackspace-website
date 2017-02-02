from autofixture import AutoFixture
from django.core.management.base import BaseCommand
from mhackspace.feeds.models import Article
from mhackspace.users.models import User


class Command(BaseCommand):
    help = 'Imports the RSS feeds from active blogs'

    def handle(self, *args, **options):
        users = AutoFixture(User)
        users.create(10)

        feeds = AutoFixture(User)
        feeds.create(10)

        self.stdout.write(
            self.style.SUCCESS(
                'Finished creating test data'))
