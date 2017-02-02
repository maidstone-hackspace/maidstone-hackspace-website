# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

from .models import Blurb

class BlurbForm(ModelForm):
    class Meta:
        model = Blurb
        exclude = ['user']
