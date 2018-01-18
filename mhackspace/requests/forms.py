from django import forms
from mhackspace.requests.models import UserRequest, UserRequestsComment


class UserRequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        exclude = ['user', 'created_date', 'acquired']


class UserRequestFormComment(forms.ModelForm):
    class Meta:
        model = UserRequestsComment
        exclude = ['user', 'created_date', 'request']
