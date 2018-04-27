from django.conf import settings
from django.contrib.auth.models import Group
from ldap3 import Server, Connection, ObjectDef, AttrDef, Reader, Writer, ALL
from celery import shared_task
import json


server = Server(settings.LDAP_SERVER)
conn = Connection(
    server,
    'cn=admin, dc=maidstone-hackspace, dc=org, dc=uk',
    settings.LDAP_PASSWORD,
    auto_bind=True)


def ldap_list_organizational_units(connection):
    connection.search(
        '%s' % (settings.LDAP_ROOT),
        '(objectclass=organizationalUnit)')
    for result in connection.entries:
        yield result


def ldap_list_groups(connection):
    connection.search(
        '%s' % (settings.LDAP_ROOT),
        '(objectclass=groupOfNames)')
    for result in connection.entries:
        yield result


def ldap_list_users(connection):
    connection.search(
        '%s' % (settings.LDAP_ROOT),
        '(objectclass=person)')
    for result in connection.entries:
        yield result



@shared_task
def ldap_add_organizational_unit(connection, name):
    exists = connection.search(
        'cn=%s, %s' % (name, settings.LDAP_ROOT),
        '(objectclass=organizationalUnit)')

    if exists is False:
        connection.add(
            'ou=%s, %s' % (name, settings.LDAP_ROOT),
            'organizationalUnit')
    return connection.result


@shared_task
def ldap_add_group(connection, group, users):
    exists = connection.search(
        'cn=%s, ou=groups, %s' % (group, settings.LDAP_ROOT),
        '(objectclass=groupOfNames)')

    cn_list = ['cn=' + u for u in users]
    g = {'objectClass':  ['groupOfNames', 'top'], 'cn': group, 'member': cn_list}
    if exists is False:
        connection.add(
            'cn=%s, ou=groups, %s' % (group, settings.LDAP_ROOT),
            attributes=g)
    return connection.result



@shared_task
def ldap_add_user(connection, username, name='', password=None):
    u = {'objectClass':  ['inetOrgPerson', 'person', 'top'], 'sn': 'user_sn', 'cn': 'First Last', 'userPassword': ''}
    if not password:
        return

    exists = connection.search(
        'cn=%s, ou=users, %s' % (username, settings.LDAP_ROOT),
        '(objectclass=inetOrgPerson)')

    u = {
        'objectClass':  ['inetOrgPerson', 'person', 'top'],
        'sn': 'user_sn',
        'cn': 'First Last name',
        'userPassword': password,
        }
    if exists is False:
        connection.add(
            'cn=%s, ou=users, %s' % (username, settings.LDAP_ROOT),
            attributes=u)
    return connection.result


@shared_task
def complete_directory_sync(self):
    server = Server(settings.LDAP_SERVER)
    conn = Connection(
        server,
        'cn=admin, dc=maidstone-hackspace, dc=org, dc=uk',
        settings.LDAP_PASSWORD,
        auto_bind=True)

    for user in User.objects.all():
        ldap_add_user(conn, user.username)
