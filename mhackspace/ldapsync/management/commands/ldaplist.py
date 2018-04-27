from django.core.management.base import BaseCommand
from mhackspace.ldapsync.tasks import (
    ldap_list_users, ldap_list_groups, ldap_list_organizational_units, conn)


class Command(BaseCommand):
    help = 'List database directory'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Listing Organizational units.....'))
        for row in ldap_list_organizational_units(conn):
            self.stdout.write(self.style.NOTICE('\t%s' % row.entry_dn))

        self.stdout.write(self.style.NOTICE('Listing Users.....'))
        for row in ldap_list_users(conn):
            self.stdout.write(self.style.NOTICE('\t%s' % row.entry_dn))

        self.stdout.write(self.style.NOTICE('Listing Groups.....'))
        for row in ldap_list_groups(conn):
            self.stdout.write(self.style.NOTICE('\t%s' % row.entry_dn))
