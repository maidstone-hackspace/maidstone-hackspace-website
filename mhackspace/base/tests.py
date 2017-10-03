from test_plus.test import TestCase
from mhackspace.users.models import Membership
from mhackspace.users.models import User
from django.contrib.auth.models import Group

from mhackspace.subscriptions.management.commands.update_membership_status import update_subscriptions

# this needs mocking
class TestTasks(TestCase):
    def setUp(self):
        self.user1 = self.make_user('u1')
        self.user2 = self.make_user('u2')
        self.group = Group(name='members')
        self.group.save()

    def test_refresh_subscriptions(self):
        membership_count = Membership.objects.all().delete()
        user_count = User.objects.all().count()
        membership_count = Membership.objects.all().count()
        self.assertEquals(0, membership_count)
        self.assertEquals(2, user_count)

        update_subscriptions(provider_name='gocardless')

        membership_count = Membership.objects.all().count()
        self.assertEquals(2, membership_count)
        self.assertEquals(2, user_count)
