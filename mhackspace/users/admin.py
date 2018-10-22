# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.admin import ModelAdmin
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf.urls import url
from .models import User, Rfid, Membership, MEMBERSHIP_STATUS_CHOICES

# from mhackspace.subscriptions.management.commands.update_membership_status import update_subscriptions
from mhackspace.users.tasks import update_users_memebership_status


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
            ('User Profile', {'fields': ('name', '_image')}),
    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'name', 'is_superuser')
    search_fields = ['name']


@admin.register(Membership)
class MembershipAdmin(ModelAdmin):
    list_display = ('user_id', 'join_date','email', 'payment', 'payment_date', 'status')
    list_filter = ('status',)

    def get_urls(self):
        urls = super(MembershipAdmin, self).get_urls()
        my_urls = [
            url(r'^refresh/payments/$', self.admin_site.admin_view(self.refresh_payments))
        ]
        return my_urls + urls

    def refresh_payments(self, request):
        update_users_memebership_status.apply_async()
        # for user in update_subscriptions(provider_name='gocardless'):
        #     continue
        self.message_user(request, 'Successfully triggered user payment refresh')
        return HttpResponseRedirect(reverse('admin:index'))


@admin.register(Rfid)
class RfidAdmin(ModelAdmin):
    list_display = ('code', 'description')
