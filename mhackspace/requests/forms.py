from django import forms
from mhackspace.requests.models import UserRequests
from mhackspace.requests.models import REQUEST_TYPES


class UserRequestForm(forms.ModelForm):
    class Meta:
        model = UserRequests
        exclude = ['user', 'created_date']
    # description = forms.CharField(
    #     required=True,
    #     widget=forms.Textarea
    # )
    # request_type = forms.ChoiceField(
    #     required=True,
    #     widget=forms.Select,
    #     choices=REQUEST_TYPES)
