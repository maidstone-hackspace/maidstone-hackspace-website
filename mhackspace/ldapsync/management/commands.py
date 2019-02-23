from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.core.management.base import BaseCommand
from mhackspace.subscriptions.payments import select_provider
from mhackspace.users.models import Membership, User
from mhackspace.subscriptions.helper import create_or_update_membership

from django.contrib.auth.models import Group
#from ldap3 import Server, Connection, ObjectDef, AttrDef, Reader, Writer, ALL
from huey.contrib.djhuey import periodic_task, task
from .models import User


class Command(BaseCommand):
    help = 'Sync database directory'

    def handle(self, *args, **options):
        for user in User.objects.all():
            self.stdout.write(self.style.NOTICE('test %s' % user.username))
        for group in Group.objects.all():
            self.stdout.write(self.style.NOTICE('test %s' % group.name))

