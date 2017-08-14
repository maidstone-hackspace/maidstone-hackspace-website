from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.core.management.base import BaseCommand
from mhackspace.subscriptions.payments import select_provider
from mhackspace.users.models import Membership, User
from mhackspace.subscriptions.helper import create_or_update_membership


def update_subscriptions(provider_name):
    provider = select_provider('gocardless')

    Membership.objects.all().delete()
    subscriptions = []

    group = Group.objects.get(name='members')

    for sub in provider.fetch_subscriptions():
        try:
            user_model = User.objects.get(email=sub.get('email'))
            if sub.get('status') == 'active':
                user_model.groups.add(group)
        except User.DoesNotExist:
            user_model = None

        subscriptions.append(
            Membership(
                user=user_model,
                email=sub.get('email'),
                reference=sub.get('reference'),
                payment=10.00,
                date= sub.get('start_date'),
                # date=timezone.now(),
                status=Membership.lookup_status(name=sub.get('status'))
            )
        )
        yield model_to_dict(subscriptions[-1])


class Command(BaseCommand):
    help = 'Update user subscriptions'

    def handle(self, *args, **options):
        provider_name = 'gocardless'
        self.stdout.write(
            self.style.NOTICE(
                '== %s subscriptions ==' % provider_name.capitalize()))

        provider = select_provider('gocardless')
        Membership.objects.all().delete()
        subscriptions = []

        group = Group.objects.get(name='members')

        for sub in provider.fetch_subscriptions():
            sub['amount'] = sub['amount'] * 0.01
            try:
                user_model = User.objects.get(email=sub.get('email'))
                if sub.get('status') == 'active':
                    user_model.groups.add(group)
            except User.DoesNotExist:
                user_model = None
                self.style.NOTICE(
                    '\tMissing User {reference} - {payment} - {status} - {email}'.format(**{
                        'reference': sub.get('reference'),
                        'payment': sub.get('amount'),
                        'status': sub.get('status'),
                        'email': sub.get('email')
                    }))
                continue

            create_or_update_membership(user=user_model,
                                        signup_details=sub,
                                        complete=True)
            subscriptions.append(
                Membership(
                    user=user_model,
                    email=sub.get('email'),
                    reference=sub.get('reference'),
                    payment=sub.get('amount'),
                    date=sub.get('start_date'),
                    status=Membership.lookup_status(name=sub.get('status'))
                )
            )

            self.stdout.write(
                self.style.SUCCESS(
                    '\t{reference} - {payment} - {status} - {email}'.format(**{
                        'reference': sub.get('reference'),
                        'payment': sub.get('amount'),
                        'status': sub.get('status'),
                        'email': sub.get('email')
                    })))

        Membership.objects.bulk_create(subscriptions)

