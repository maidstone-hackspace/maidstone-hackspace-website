from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.core.management.base import BaseCommand
from mhackspace.subscriptions.payments import select_provider
from mhackspace.users.models import Membership, User
from mhackspace.subscriptions.helper import create_or_update_membership


# this should be done in bulk, create the objects and save all at once
# for now its not an issue, because of small membership size


def update_subscriptions(provider_name):
    provider = select_provider('gocardless')

    Membership.objects.all().delete()

    group = Group.objects.get(name='members')

    for sub in provider.fetch_subscriptions():
        try:
            user_model = User.objects.get(email=sub.get('email'))
            if sub.get('status') == 'active':
                user_model.groups.add(group)
        except User.DoesNotExist:
            user_model = None

        create_or_update_membership(
            user=user_model,
            signup_details=sub,
            complete=True)


class Command(BaseCommand):
    help = 'Update user subscriptions'

    def handle(self, *args, **options):
        provider_name = 'gocardless'
        self.stdout.write(
            self.style.NOTICE(
                '== %s subscriptions ==' % provider_name.capitalize()))

        provider = select_provider('gocardless')
        Membership.objects.all().delete()

        group = Group.objects.get(name='members')

        for sub in provider.fetch_subscriptions():
            prefix = ''
            sub['amount'] = sub['amount'] * 0.01
            try:
                user_model = User.objects.get(email=sub.get('email'))
                if sub.get('status') == 'active':
                    user_model.groups.add(group)
            except User.DoesNotExist:
                user_model = None
                prefix = 'NO USER - '

            create_or_update_membership(user=user_model,
                                        signup_details=sub,
                                        complete=True)

            message = '\t{prefix}{date} - {reference} - {payment} - {status} - {email}'.format(**{
                'prefix': prefix,
                'date': sub.get('start_date'),
                'reference': sub.get('reference'),
                'payment': sub.get('amount'),
                'status': sub.get('status'),
                'email': sub.get('email')
            })

            if user_model:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.NOTICE(message))

