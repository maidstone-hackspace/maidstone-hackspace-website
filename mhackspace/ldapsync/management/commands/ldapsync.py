from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from mhackspace.users.models import User
from mhackspace.ldapsync.tasks import (
    ldap_add_user, ldap_add_group, ldap_add_organizational_unit, conn)


class Command(BaseCommand):
    help = 'Sync database directory'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Loading Organizational unit.....'))

        ldap_add_organizational_unit(conn, 'users')
        ldap_add_organizational_unit(conn, 'groups')

        self.stdout.write(self.style.NOTICE('Loading Users.....'))

        for user in User.objects.all():
            result = ldap_add_user(
                conn,
                username=user.username,
                password=user.password)
            if result.get('message'):
                self.stdout.write(result.get('message'))
            self.stdout.write(self.style.NOTICE('\ttest %s' % user.username))

        self.stdout.write(self.style.NOTICE('Loading Groups.....'))

        for group in Group.objects.all():
            result = ldap_add_group(conn, group.name, ['admin', ])
            if result.get('message'):
                self.stdout.write(result.get('message'))

            self.stdout.write(self.style.NOTICE('\ttest %s' % group.name))
