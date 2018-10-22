from autofixture import AutoFixture
from autofixture.generators import ImageGenerator
from django.core.management.base import BaseCommand
from django.core.management import call_command
from mhackspace.base.models import BannerImage
from mhackspace.feeds.models import Article, Feed
from mhackspace.users.models import User


class Command(BaseCommand):
    help = 'Build test data for development environment'

    def handle(self, *args, **options):
        try:
            # python2
            from urllib import urlretrieve
        except ImportError:
            # python3
            from urllib.request import urlretrieve

        from martor.extensions.emoji import EMOJIS

        emoji_path = 'mhackspace/static/images/emojis/' # create this folder first
        base_url = 'https://assets-cdn.github.com/images/icons/emoji/'

        for emoji in EMOJIS:
            emoji_image = emoji.replace(':', '') + '.png'

            urlretrieve(base_url + emoji_image, emoji_path + emoji_image)
            print("Downloaded: {}".format(emoji_image))
