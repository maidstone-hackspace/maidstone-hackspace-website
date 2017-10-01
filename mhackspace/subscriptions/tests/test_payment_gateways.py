#!/usr/bin/env python
# -*- coding: utf-8 -*-
from test_plus.test import TestCase
from unittest import skip
from mock import patch, Mock, MagicMock
from mhackspace.users.models import Membership
import django.utils.timezone

from mhackspace.subscriptions.payments import gocardless_provider, braintree_provider
from mhackspace.subscriptions.tests.mocks import gocardlessMocks


class TestPaymentGatewaysGocardless(gocardlessMocks):

    def setUp(self):
        super().setUp()
        # self.date_now = django.utils.timezone.now()
        # self.user = self.make_user()
        # member = Membership()
        # member.user = self.user
        # member.payment = '20.00'
        # member.date = self.date_now
        # member.save()
        # self.auth_gocardless()


    @skip("Need to implement")
    @patch('mhackspace.subscriptions.payments.gocardless_pro.Client.subscription', autospec=True)
    def test_unsubscribe(self, mock_subscription):
        self.mock_success_responses()
        # self.auth_gocardless()
        mock_subscription.return_value = Mock(success='success')
        mock_subscription.cancel.return_value = Mock(
            id='01',
            status='active',
            amount=20.00,
            created_at='date'
        )
        result = self.provider.cancel_subscription(reference='M01')

        self.assertEqual(result.get('amount'), 20.00)
        self.assertEqual(result.get('reference'), '02')
        self.assertEqual(result.get('success'), 'success')

    def test_confirm_subscription_callback(self):
        self.mock_success_responses()
        membership = self.create_membership_record()
        # self.auth_gocardless()
        # mock_confirm.return_value = Mock(success='success')

        request_params = {
            'resource_uri': 'http://gocardless/resource/url/01',
            'resource_id': '01',
            'resource_type': 'subscription',
            'signature': 'sig',
            'state': 'inactive'
        }


        # membership = Membership.objects.get(user=self.user)
        result = self.provider.confirm_subscription(
            membership=membership,
            session=None,
            provider_response={'redirect_flow_id': 'redirect_mock_url'},
            name='test')

        self.assertEqual(result.get('amount'), '20.00')
        self.assertEqual(result.get('reference'), '02')
        self.assertEqual(result.get('success'), '200')

    def test_fetch_subscription_gocardless(self):
        self.mock_success_responses()
        for item in self.provider.fetch_subscriptions():
            self.assertEqual(item.get('status'), 'active')
            self.assertEqual(item.get('email'), 'test@test.com')
            self.assertEqual(item.get('reference'), '01')
            self.assertEqual(item.get('amount'), 20.00)

