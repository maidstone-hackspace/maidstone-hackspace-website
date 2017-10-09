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
                '== Gocardless customer payments =='))

        Payments.objects.all().delete()

        payment_objects = []
        for customer in provider.fetch_customers():
            user = User.objects.get(email=customer.get('email')) 
            payment_objects.append(Payments(
                user=user,
                user_reference=customer.get('user_reference'),
                user_email=customer.get('email'),
                reference=customer.get('payment_id'),
                amount=customer.get('amount'),
                type=Payments.lookup_payment_type(customer.get('payment_type')),
                date=customer.get('payment_date')
            ))
            self.stdout.write(
                self.style.SUCCESS(
                    '\t{reference} - {amount} - {type} - {user_email}'.format(**model_to_dict(payment_objects[-1]))))



        Payments.objects.bulk_create(payment_objects)
