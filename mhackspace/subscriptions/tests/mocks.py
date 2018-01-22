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

    def mock_success_responses(self, responses=None):
        if responses == None:
        subscription_properties = Mock(
            id='02',
            status='active',
            amount=20.00,
            created_at='date'
        )

        mock_list = MagicMock()
        mock_list_records = MagicMock(side_effect=[subscription_properties])
        mock_list.records.return_value = mock_list_records

        self.provider.client.subscriptions.list = mock_list
        ApiResponse = namedtuple('ApiResponse', 'api_response, created_at')
        ApiResponseStatus = namedtuple('ApiResponseStatus', 'status_code')

        self.provider.client.subscriptions.create = Mock(
            return_value=ApiResponse(
                created_at=self.date_now,
                api_response=ApiResponseStatus(status_code='200'))
        )

        self.provider.client.subscriptions.get = Mock(
            return_value=subscription_properties)

        self.provider.client.subscriptions.cancel = PropertyMock(
            return_value={'status_code': '200'})


    def mock_success_responses2(self, responses=None):
        if responses == None:
            responses = [Mock(
                id='02',
                status='active',
                amount=20.00,
                created_at='date'
            )]

        mock_list = MagicMock()
        mock_list_records = MagicMock(side_effect=[subscription_properties])
        mock_list.records.return_value = mock_list_records

        self.provider.client.subscriptions.list = mock_list
        ApiResponse = namedtuple('ApiResponse', 'api_response, created_at')
        ApiResponseStatus = namedtuple('ApiResponseStatus', 'status_code')

        self.provider.client.subscriptions.create = Mock(
            return_value=ApiResponse(
                created_at=self.date_now,
                api_response=ApiResponseStatus(status_code='200'))
        )

        self.provider.client.subscriptions.get.side_effects = responses
        self.provider.client.subscriptions.cancel = PropertyMock(
            return_value={'status_code': '200'})

