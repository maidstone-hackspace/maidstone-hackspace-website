from django.core.management.base import BaseCommand
from mhackspace.subscriptions.payments import select_provider


class Command(BaseCommand):
    help = 'List payment provider subscriptions'

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         'blog_id',
    #         nargs='*',
    #         type=int,
    #         default=False,
    #         help='Specify a blog to get feeds form'
    #     )

    def handle(self, *args, **options):
        provider = select_provider('gocardless')

        self.stdout.write(
            self.style.NOTICE(
                '== Gocardless subscriptions =='))

        for sub in provider.fetch_subscriptions():
            self.stdout.write(
                self.style.SUCCESS(
                    '\t{reference} - {amount} - {status} - {email}'.format(**sub)))
