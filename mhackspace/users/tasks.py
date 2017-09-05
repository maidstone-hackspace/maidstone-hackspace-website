from celery import shared_task
from mhackspace.subscriptions.management.commands.update_membership_status import update_subscriptions


@shared_task
def update_users_memebership_status():
    for user in update_subscriptions(provider_name='gocardless'):
        continue
