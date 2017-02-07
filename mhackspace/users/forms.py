# -*- coding: utf-8 -*-
from django.db import models
from django import forms

from .models import Blurb

PAYMENT_PROVIDERS = (
    ('gocardless', 'GoCardless'),
    # ('braintree', 'Braintree'),
)
class BlurbForm(forms.ModelForm):
    class Meta:
        model = Blurb
        exclude = ['user']

class MembershipJoinForm(forms.Form):
    payment_provider = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=PAYMENT_PROVIDERS)

    amount = forms.DecimalField(required=True, decimal_places=2)
