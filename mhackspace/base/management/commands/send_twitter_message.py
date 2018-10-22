from django.core.management.base import BaseCommand
from django.core.management import call_command
from mhackspace.base.tasks import twitter_message


class Command(BaseCommand):
    help = 'Build test data for development environment'

    def handle(self, *args, **options):
        twitter_message('Test twitter message')
        print("Sent Message via twitter")
