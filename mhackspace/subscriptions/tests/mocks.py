from test_plus.test import TestCase
from mock import patch, Mock, MagicMock, PropertyMock
from mhackspace.users.models import Membership
import django.utils.timezone
from collections import namedtuple

from mhackspace.subscriptions.payments import gocardless_provider


class gocardlessMocks(TestCase):

    def setUp(self):
        self.date_now = django.utils.timezone.now()
        self.user1 = self.make_user()
        self.auth_gocardless()

    def create_membership_record(self):
        member = Membership()
        member.user = self.user1
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

    def mock_success_responses_old(self, responses=None):
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

    def mock_customer_success_responses(self):
        ApiCustomersGet = namedtuple('ApiCustomersGet', 'email')
        self.provider.client.customers.get = Mock(
            return_value=ApiCustomersGet(
                email='test@test.com')
        )

    def mock_mandate_success_responses(self):
        ApiSubscriptionMandateLink = namedtuple('ApiSubscriptionMandateLink', 'customer')
        # ApiMandateGet = namedtuple('ApiMandateGet', '')
        self.provider.client.mandates.get = Mock()

    def mock_success_responses(self, responses=None):
        if responses is None:
            responses = Mock(
                id='02',
                status='active',
                amount=20.00,
                created_at='date'
            )

        ApiRecords = namedtuple('ApiRecords', 'records')
        ApiMandateLink = namedtuple('ApiMandateLink', 'mandate')
        ApiResponseSubscriptionList = namedtuple('ApiResponseSubscriptionList', 'id, created_at, status, amount, links')
        self.provider.client.subscriptions.list = Mock(
            return_value=ApiRecords(
                records=[
                    ApiResponseSubscriptionList(
                        id='02',
                        status='active',
                        created_at=self.date_now,
                        amount=2000,
                        links=ApiMandateLink(
                            mandate='mid01'
                        )
                )]
            )
        )

        ApiResponseGet = namedtuple('ApiResponseGet', 'api_response, id, status, amount, created_at')
        ApiResponseCreate = namedtuple('ApiResponseCreate', 'api_response, id, status, created_at')
        ApiResponseCancelled = namedtuple('ApiResponseCancelled', 'api_response, status')
        ApiResponseStatus = namedtuple('ApiResponseStatus', 'status_code')

        self.provider.client.subscriptions.create = Mock(
            return_value=ApiResponseCreate(
                id='02',
                status='active',
                created_at=self.date_now,
                api_response=ApiResponseStatus(status_code='200'))
        )

        self.provider.client.subscriptions.get = Mock(
            return_value=ApiResponseGet(
                id='02',
                created_at=self.date_now,
                amount=20.00,
                status='active',
                api_response=ApiResponseStatus(status_code='200'))
            )


        self.provider.client.subscriptions.cancel = Mock(

            return_value=ApiResponseCancelled(
                api_response=ApiResponseStatus(status_code='200'),
                status='cancelled'))


        # self.provider.client.subscriptions.cancel = PropertyMock(
        #     return_value={'status_code': '200'})


