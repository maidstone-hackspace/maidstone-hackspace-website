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

    def test_unsubscribe(self):
        responses = [
            Mock(
                id='02',
                status='active',
                amount=20.00,
                created_at='date'
            ), Mock(
                id='03',
                status='active2',
                amount=40.00,
                created_at='date'
            ),
        ]
        self.mock_success_responses2(responses)

        result = self.provider.cancel_subscription(user=self.user, reference='M01')

        self.assertEqual(result.get('amount'), 20.00)
        self.assertEqual(result.get('reference'), '02')
        self.assertEqual(result.get('success'), True)

    def test_confirm_subscription_callback(self):
        self.mock_success_responses()
        membership = self.create_membership_record()

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
            self.assertEqual(item.get('reference'), '02')
            self.assertEqual(item.get('amount'), 20.00)

