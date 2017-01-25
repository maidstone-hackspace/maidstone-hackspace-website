#!/usr/bin/env python
# -*- coding: utf-8 -*-
from test_plus.test import TestCase
# import unittest
from mock import patch, Mock

from mhackspace.subscriptions.payments import payment, gocardless_provider, braintree_provider

class TestPaymentGatewaysGocardless(TestCase):

    def setUp(self):
        self.auth_gocardless()

    @patch('mhackspace.subscriptions.payments.gocardless.request.requests.get', autospec=True)
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

    def test_confirm_subscription_callback(self):
        with patch('gocardless.client.confirm_resources') as mock_subscription:
            self.provider = gocardless_provider()

    def test_fetch_subscription_gocardless(self):
        items = [Mock(
            id='01',
            status='active',
            amount=20.00,
            reference='ref01',
            created_at='date'
        )]
        items[-1].user.return_value = Mock(email='test@test.com')

        self.provider.client = Mock()
        self.provider.client.subscriptions = Mock(return_value=items)
        for item in self.provider.fetch_subscriptions():
            self.assertEqual(item.get('status'), 'active')
            self.assertEqual(item.get('email'), 'test@test.com')
            self.assertEqual(item.get('reference'), 'ref01')
            self.assertEqual(item.get('start_date'), 'date')
            self.assertEqual(item.get('amount'), 20.00)


class TestPaymentGatewaysBraintree(TestCase):
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
