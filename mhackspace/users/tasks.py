from huey.contrib.djhuey import periodic_task, task
from mhackspace.subscriptions.management.commands.update_membership_status import update_subscriptions


@task()
def update_users_memebership_status():
    update_subscriptions(provider_name='gocardless')
