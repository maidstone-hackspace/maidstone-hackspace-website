# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib import messages
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

from django.views.generic import UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin

from mhackspace.users.models import User
from mhackspace.users.forms import MembershipJoinForm
from mhackspace.subscriptions.payments import select_provider

class MembershipJoinView(LoginRequiredMixin, UpdateView):
    model = User
    fields = []

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        app_domain = 'http://test.maidstone-hackspace.org.uk'
        payment_provider = 'gocardless'
        provider = select_provider(payment_provider)
        user_code =  str(self.request.user.id).zfill(5)

        form_subscription = MembershipJoinForm(data=self.request.POST)
        form_subscription.is_valid()

        success_url = '%s/membership/%s/success' % (app_domain, payment_provider)
        failure_url = '%s/membership/%s/failure' % (app_domain, payment_provider)
        url = provider.create_subscription(
            amount=form_subscription.cleaned_data.get('amount', 20.00),
            name="Membership your membership id is MH%s" % user_code,
            redirect_success=success_url,
            redirect_failure=failure_url
        )

        return redirect(url)


class MembershipJoinSuccessView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = 'users:detail'

    def get_redirect_url(self, *args, **kwargs):
        del(kwargs['provider'])
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Success your membership should now be active')
        kwargs['username'] =  self.request.user.get_username()
        return super(MembershipJoinSuccessView, self).get_redirect_url(*args, **kwargs)


class MembershipJoinFailureView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = 'users:detail'

    def get_redirect_url(self, *args, **kwargs):
        del(kwargs['provider'])
        messages.add_message(
            self.request,
            messages.ERROR,
            'Failed to sign up something went wrong with your payment')
        kwargs['username'] =  self.request.user.get_username()
        return super(MembershipJoinFailureView, self).get_redirect_url(*args, **kwargs)
