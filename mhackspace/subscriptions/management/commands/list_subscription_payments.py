from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.core.management.base import BaseCommand
from mhackspace.subscriptions.payments import select_provider
from mhackspace.users.models import Membership, User
from mhackspace.subscriptions.models import Payments


class Command(BaseCommand):
    help = 'Update user subscriptions'

    def handle(self, *args, **options):
        provider = select_provider('gocardless')

        self.stdout.write(
            self.style.NOTICE(
                '== Gocardless customers =='))

        Payments.objects.all().delete()
        for customer in provider.fetch_customers():
            self.stdout.write(str(dir(customer)))
            self.stdout.write(str(customer))

            Payments.objects.create(
                user=None,
                user_reference=customer.get('user_id'),
                user_email=customer.get('email'),
                reference=customer.get('payment_id'),
                amount=customer.get('amount'),
                type=Payments.lookup_payment_type(customer.get('payment_type')),
                date=customer.get('payment_date')
            )
            # self.stdout.write(str(customer.email))
            # self.stdout.write(str(dir(customer['email']())))
            # self.stdout.write(
            #     self.style.SUCCESS(
            #         '\t{reference} - {payment} - {status} - {email}'.format(**model_to_dict(subscriptions[-1]))))


