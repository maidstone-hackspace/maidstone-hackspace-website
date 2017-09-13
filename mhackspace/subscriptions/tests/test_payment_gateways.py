#!/usr/bin/env python
# -*- coding: utf-8 -*-
from test_plus.test import TestCase
from unittest import skip
from mock import patch, Mock

from mhackspace.subscriptions.payments import payment, gocardless_provider, braintree_provider


class TestPaymentGatewaysGocardless(TestCase):

    def setUp(self):
        self.auth_gocardless()

    @patch('mhackspace.subscriptions.payments.gocardless_pro.request.requests.get', autospec=True)
    def auth_gocardless(self, mock_request):
        # mock braintree initalisation request
        mock_request.return_value = Mock(ok=True)
        mock_request.return_value.json.return_value = {
            "id": "1",
            "created_at": "2011-11-18T17:07:09Z",
            "access_token": "test_token",
            "next_payout_date": "2011-11-18T17:07:09Z"
        }

        with patch('gocardless.resources.Merchant') as mock_subscription:
            self.provider = gocardless_provider()
        return self.provider #self.provider

    @skip("Need to implement")
    @patch('mhackspace.subscriptions.payments.gocardless_pro.client.subscription', autospec=True)
    def test_unsubscribe(self, mock_subscription):
        mock_subscription.return_value = Mock(success='success')
        mock_subscription.cancel.return_value = Mock(
            id='01',
            status='active',
            amount=20.00,
            created_at='date'
        )
        result = self.provider.cancel_subscription(reference='M01')

        self.assertEqual(result.get('amount'), 20.00)
        self.assertEqual(result.get('start_date'), 'date')
        self.assertEqual(result.get('reference'), '01')
        self.assertEqual(result.get('success'), 'success')

    @patch('mhackspace.subscriptions.payments.gocardless_pro.client.subscription', autospec=True)
    @patch('mhackspace.subscriptions.payments.gocardless_pro.client.confirm_resource', autospec=True)
    def test_confirm_subscription_callback(self, mock_confirm, mock_subscription):
        mock_confirm.return_value = Mock(success='success')
        mock_subscription.return_value = Mock(
            id='01',
            status='active',
            amount=20.00,
            created_at='date'
        )

        request_params = {
            'resource_uri': 'http://gocardless/resource/url/01',
            'resource_id': '01',
            'resource_type': 'subscription',
            'signature': 'sig',
            'state': 'inactive'
        }

        result = self.provider.subscribe_confirm(request_params)

        self.assertEqual(result.get('amount'), 20.00)
        self.assertEqual(result.get('start_date'), 'date')
        self.assertEqual(result.get('reference'), '01')
        self.assertEqual(result.get('success'), 'success')


    def test_fetch_subscription_gocardless(self):
        item = Mock(
            id='01',
            status='active',
            amount=20.00,
            created_at='date'
        )
        item.user.return_value = Mock(email='test@test.com')

        self.provider.client = Mock()
        self.provider.client.subscriptions = Mock(return_value=[item])

        # mock out gocardless subscriptions method, and return our own values
        for item in self.provider.fetch_subscriptions():
            self.assertEqual(item.get('status'), 'active')
            self.assertEqual(item.get('email'), 'test@test.com')
            self.assertEqual(item.get('reference'), '01')
            self.assertEqual(item.get('start_date'), 'date')
            self.assertEqual(item.get('amount'), 20.00)


class DisabledestPaymentGatewaysBraintree(TestCase):
    @patch('mhackspace.subscriptions.payments.braintree.Configuration.configure')
    def auth_braintree(self, mock_request):
        # mock braintree initalisation request
        mock_request.return_value = Mock(ok=True)
        mock_request.return_value.json.return_value = {
            "id": "1",
            "created_at": "2011-11-18T17:07:09Z",
            "access_token": "test_token",
            "next_payout_date": "2011-11-18T17:07:09Z"
        }

        self.provider = braintree_provider()

    @patch('mhackspace.subscriptions.payments.braintree.Subscription.search')
    def test_fetch_subscription_braintree(self, mock_request):
        provider = self.auth_braintree()

        items = [Mock(
           id='01',
           status='active',
           amount=20.00,
           reference='ref01',
           created_at='date'
        )]
        items[-1].user.return_value = Mock(email='test@test.com')

        mock_request.return_value = items 
        for item in self.provider.fetch_subscriptions():
            self.assertEqual(item.get('status'), 'active')
            self.assertEqual(item.get('email'), 'test@test.com')
            self.assertEqual(item.get('reference'), 'ref01')
            self.assertEqual(item.get('start_date'), 'date')
            self.assertEqual(item.get('amount'), 20.00)
