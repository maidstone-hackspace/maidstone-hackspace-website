from django import forms
from mhackspace.register.models import RegisteredUser


class RegisteredUserForm(forms.ModelForm):
    class Meta:
        model = RegisteredUser
        exclude = ['user', 'created_at']
