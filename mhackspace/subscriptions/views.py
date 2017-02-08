# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

from django.views.generic import UpdateView
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

        success_url = '%s/profile/membership/%s/success' % (app_domain, payment_provider)
        failure_url = '%s/profile/membership/%s/failure' % (app_domain, payment_provider)
        url = provider.create_subscription(
            amount=form_subscription.cleaned_data.get('amount', 20.00),
            name="Membership your membership id is MH%s" % user_code,
            redirect_success=success_url,
            redirect_failure=failure_url
        )

        return redirect(url)
