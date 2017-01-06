# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

from .models import UserBlurb

class UserBlurbForm(ModelForm):
    class Meta:
        model = UserBlurb
        exclude = ['user']
