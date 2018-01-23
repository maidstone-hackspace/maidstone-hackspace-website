import mock
from test_plus.test import TestCase
from mhackspace.users.models import Membership
from mhackspace.users.models import User
from django.contrib.auth.models import Group

from mhackspace.subscriptions.management.commands.update_membership_status import update_subscriptions

from mhackspace.subscriptions.tests.mocks import gocardlessMocks

# this needs mocking
class TestTasks(gocardlessMocks):
    def setUp(self):
        super().setUp()
        self.user2 = self.make_user('u2')
        self.user3 = self.make_user('u3')
        self.group = Group(name='members')
        self.group.save()

    @mock.patch('mhackspace.subscriptions.payments.select_provider')
    def test_refresh_subscriptions(self, mock_select_provider):
        self.mock_success_responses()
        self.mock_mandate_success_responses()
        self.mock_customer_success_responses()
        mock_select_provider.return_value = self.provider

        membership_count = Membership.objects.all().delete()
        user_count = User.objects.all().count()
        membership_count = Membership.objects.all().count()
        self.assertEquals(0, membership_count)
        self.assertEquals(3, user_count)

        update_subscriptions(provider_name='gocardless')

        self.mock_success_responses()

        membership_count = Membership.objects.all().count()
        self.assertEquals(2, membership_count)
        self.assertEquals(2, user_count)
