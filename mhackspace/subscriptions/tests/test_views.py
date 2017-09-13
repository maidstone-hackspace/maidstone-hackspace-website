from django.contrib.messages.storage.fallback import FallbackStorage
# from django.contrib.auth.models import Group
from django.test import Client
from django.test import RequestFactory
from django.core.urlresolvers import reverse
from test_plus.test import TestCase
from mock import patch, Mock
from mhackspace.users.models import Membership
from mhackspace.users.models import User

from mhackspace.subscriptions.payments import payment, gocardless_provider, braintree_provider

from ..views import (
    MembershipCancelView,
    MembershipJoinView,
    MembershipJoinSuccessView,
    MembershipJoinFailureView
)


class BaseUserTestCase(TestCase):
    fixtures = ['groups']

    def setUp(self):
        self.user = self.make_user()
        self.user.save()
        self.factory = RequestFactory()
        self.client = Client()
        self.client.login(
            username=self.user.username,
            password=self.user.password)


class TestSubscriptionSuccessRedirectView(BaseUserTestCase):
    @patch('mhackspace.subscriptions.payments.gocardless_provider', autospec=True)
    @patch('mhackspace.subscriptions.views.select_provider', autospec=True)
    def test_success_redirect_url(self, mock_subscription, mock_provider):
        mock_subscription.return_value = mock_provider
        mock_provider.confirm_subscription.return_value = {
            'amount': 20.00,
            'start_date': '2017-01-01T17:07:09Z',
            'reference': 'MH0001',
            'email': 'user@test.com',
            'success': True
        }

        response = self.client.post(
            reverse('join_hackspace_success', kwargs={'provider': 'gocardless'}), {
                'resource_id': 'R01',
                'resource_type': 'subscription',
                'resource_url': 'https://sandbox.gocardless.com',
                'signature': 'test_signature'
            },
            follow=True
        )

        # print('=============================')
        # setattr(request, 'session', 'session')
        # messages = FallbackStorage(request)
        # setattr(request, '_messages', messages)
        # request.user = user1

        # view = MembershipJoinSuccessView()
        # view.request = request
        # print(self.user)
        self.assertRedirects(
            response,
            expected_url=reverse('users:detail', kwargs={'username': self.user.username}),
            status_code=302,
            target_status_code=200)
        self.assertEqual(
            view.get_redirect_url(provider ='gocardless'),
            reverse('users:detail', kwargs={'username': self.user.username})
        )

        members = Membership.objects.all()
        self.assertEqual(members.count(), 1)

    @patch('mhackspace.subscriptions.payments.gocardless_pro.client.subscription', autospec=True)
    def test_failure_redirect_url(self, mock_obj):
        # Instantiate the view directly. Never do this outside a test!
        # Generate a fake request
        request = self.factory.post(
            reverse('join_hackspace_failure', kwargs={'provider': 'gocardless'}),
            data={'signature': 'test_signature'}
        )


        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user

        view = MembershipJoinFailureView()
        view.request = request

        self.assertEqual(
            view.get_redirect_url(provider='gocardless'),
            reverse('users:detail', kwargs={'username': self.user.username})
        )

        members = Membership.objects.all()
        self.assertEqual(len(members), 0)
