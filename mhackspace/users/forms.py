# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from allauth.account.forms import SignupForm
from .models import Blurb

PAYMENT_PROVIDERS = (
    ("gocardless", "GoCardless"),
    # ('braintree', 'Braintree'),
)


class CustomSignupForm(SignupForm):
    located = forms.ChoiceField(
        required=False,
        choices=[
            ("abc", "Birmingham, UK"),
            ("def", "Maidstone, Vermoont"),
            ("ghi", "Maidstone UK"),
            ("jkl", "London, UK"),
        ],
    )

    def clean_located(self):
        data = self.cleaned_data["located"]
        if data == "ghi":
            del (self.cleaned_data["located"])
            return data
        raise forms.ValidationError(
            "Incorrect, Please answer correctly."
        )


class BlurbForm(forms.ModelForm):
    class Meta:
        model = Blurb
        exclude = ["user"]


class MembershipJoinForm(forms.Form):
    payment_provider = forms.ChoiceField(
        required=True, widget=forms.Select, choices=PAYMENT_PROVIDERS
    )

    amount = forms.DecimalField(required=True, decimal_places=2)
    over_18 = forms.BooleanField(required=True)
