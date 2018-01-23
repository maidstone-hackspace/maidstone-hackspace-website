from pprint import pprint
import pytz
import gocardless_pro
import braintree
import logging

from django.conf import settings
payment_providers = settings.PAYMENT_PROVIDERS
logger = logging.getLogger(__name__)
# import paypalrestsdk as paypal

PROVIDER_ID = {'gocardless':1, 'braintree': 2}
PROVIDER_NAME = {1: 'gocardless', 2: 'braintree'}


def select_provider(type):
    if type == "gocardless": return gocardless_provider()
    if type == "braintree": return braintree_provider()
    if type == "paypal": return paypal_provider()

    log.exception('[scaffold] - "No Provider for ' + type)
    assert 0, "No Provider for " + type


class gocardless_provider:
    """
    gocardless test account details 20-00-00, 55779911
    """
    form_remote = True
    client = None

    def __init__(self):
        # gocardless are changing there api, not sure if we can switch yet
        self.client = gocardless_pro.Client(
            access_token=payment_providers['gocardless']['credentials']['access_token'],
            environment=payment_providers['gocardless']['environment'])

    def fetch_customers(self):
        """Fetch list of customers payments"""
        for customer in self.client.customers.list().records:
            for payment in self.client.payments.list(params={"customer": customer.id}).records:
                yield {
                    'user_reference': customer.id,
                    'email': customer.email,
                    'status': payment.status,
                    'payment_id': payment.links.subscription,
                    'payment_type': 'subscription' if payment.links.subscription else 'payment',
                    'payment_date': payment.created_at,
                    'amount': payment.amount
                }


    def fetch_subscriptions(self):
        # for paying_member in self.client.mandates.list().records:
        print('#############')
        print(self.client.subscriptions.list())
        print(self.client.subscriptions.list().records)
        for paying_member in self.client.subscriptions.list().records:
            mandate = self.client.mandates.get(paying_member.links.mandate)
            user = self.client.customers.get(mandate.links.customer)

            # gocardless does not have a reference so we use the id instead
            yield {
                'status': paying_member.status,
                'email': user.email,
                'start_date': paying_member.created_at,
                'reference': paying_member.id,
                'amount': paying_member.amount * 0.01}

    def get_redirect_url(self):
        return payment_providers['gocardless']['redirect_url']

    def get_token(self):
        return 'N/A'

    def cancel_subscription(self, user, reference):
        try:
            subscription = self.client.subscriptions.get(reference)
            response = self.client.subscriptions.cancel(reference)
        except gocardless_pro.errors.InvalidApiUsageError as e:
            if e.code is 404:
                logger.info('Cancel subscription failed user not found %s %s' % (e.code, e))
            return {
                'success': False
            }
        except Exception as e:
            logger.info('Cancel subscription failed unknown reason code %s %s' % (e.code, e))
            return {
                'success': False
            }
        return {
            'amount': subscription.amount,
            'start_date': subscription.created_at,
            'reference': subscription.id,
            'success': True if response.status == 'cancelled' else False
        }

    def create_subscription(self, user, session, amount,
                            name, redirect_success, redirect_failure,
                            interval_unit='monthly', interval_length='1'):
        return self.client.redirect_flows.create(params={
            "description": name,
            "session_token": session,
            "success_redirect_url": redirect_success,
            "prefilled_customer": {
                "given_name": user.first_name,
                "family_name": user.last_name,
                "email": user.email
            }
        })


    def confirm_subscription(self, membership, session, provider_response,
                             name, interval_unit='monthly', interval_length='1'):
        r = provider_response.get('redirect_flow_id')
        response = self.client.redirect_flows.complete(r, params={'session_token': session})

        user_id = response.links.customer
        mandate_id = response.links.mandate
        user = self.client.customers.get(response.links.customer)
        mandate = self.client.mandates.get(response.links.mandate)

        #  for some reason go cardless is in pence, so 20.00 needs to be sent as 2000
        #  what genious decided that was a good idea, now looks like i am charging £2000 :p
        #  the return is the same so you need to convert on send and receive
        subscription_response = self.client.subscriptions.create(
            params={
                'amount': str(membership.payment).replace('.', ''),
                'currency': 'GBP',
                'interval_unit': interval_unit,
                'name': name,
                # 'metadata': {'reference': },
                'links': {'mandate': mandate_id}
            })
        return {
            'amount': membership.payment,
            'email': user.email,
            'start_date': subscription_response.created_at,
            'reference': subscription_response.id,
            'status': subscription_response.status,
            'success': subscription_response.api_response.status_code
        }


class braintree_provider:
    form_remote = False

    def __init__(self):
        braintree.Configuration.configure(
            environment=braintree.Environment.Sandbox,
            merchant_id=payment_providers['braintree']['credentials']['merchant_id'],
            public_key=payment_providers['braintree']['credentials']['public_key'],
            private_key=payment_providers['braintree']['credentials']['private_key'])

    def get_token(self):
        return braintree.ClientToken.generate()


    def create_subscription(self, amount, name, redirect_success, redirect_failure, interval_unit='month', interval_length='1'):
        result = braintree.Customer.create({
            "first_name": "test",
            "last_name": "user",
            "payment_method_nonce": nonce_from_the_client
        })

        return braintree.Subscription.create({
            "payment_method_token": "the_token",
            "plan_id": "membership",
            "merchant_account_id": "gbp_sandbox"
            #"price": "20.00"
            #'name': name
        })

    def confirm_subscription(self, args):
        if self.provider == 'gocardless':
            response = gocardless_pro.client.confirm_resource(args)
            subscription = gocardless_pro.client.subscription(args.get('resource_id'))
            return {
                'amount': subscription.amount,
                'start_date': subscription.created_at,
                'reference': subscription.id
            }


    def fetch_subscriptions(self):
        for paying_member in braintree.Subscription.search(braintree.SubscriptionSearch.status == braintree.Subscription.Status.Active):
            user=paying_member.user()
            yield {
                'status': paying_member.status,
                'email': user.email,
                'start_date': paying_member.created_at,
                'reference': paying_member.reference,
                'amount': paying_member.amount}

