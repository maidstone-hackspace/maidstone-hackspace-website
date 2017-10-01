from test_plus.test import TestCase
from mock import patch, Mock, MagicMock, PropertyMock
from mhackspace.users.models import Membership
import django.utils.timezone
from collections import namedtuple

from mhackspace.subscriptions.payments import gocardless_provider


class gocardlessMocks(TestCase):

    def setUp(self):
        self.date_now = django.utils.timezone.now()
        self.user = self.make_user()
        self.auth_gocardless()

    def create_membership_record(self):
        member = Membership()
        member.user = self.user
        member.payment = '20.00'
        member.date = self.date_now
        member.save()
        return member

    @patch('mhackspace.subscriptions.payments.gocardless_pro', autospec=True)
    def auth_gocardless(self, mock_request):
        RedirectFlow = namedtuple('RedirectFlow', 'links')
        Links = namedtuple('Links', 'mandate, customer')
        mp = RedirectFlow(
            links=Links(mandate='02', customer='01'))

        self.provider = gocardless_provider()
        self.provider.client.redirect_flows.get = PropertyMock(return_value=mp)

        return self.provider

    def mock_success_responses(self):

        mock_list = MagicMock()
        mock_list_records = MagicMock(side_effect=[Mock(
            id='01',
            status='active',
            amount=20.00,
            created_at='date'
        )])
        mock_list.records.return_value = mock_list_records

        self.provider.client.subscriptions.list = mock_list
        ApiResponse = namedtuple('ApiResponse', 'api_response, created_at')
        ApiResponseStatus = namedtuple('ApiResponseStatus', 'status_code')

        self.provider.client.subscriptions.create = Mock(
            return_value=ApiResponse(
                created_at=self.date_now,
                api_response=ApiResponseStatus(status_code='200'))
        )
