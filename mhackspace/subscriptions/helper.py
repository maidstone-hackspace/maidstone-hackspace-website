# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.contrib import messages
from django.contrib.auth.models import Group
from mhackspace.users.models import Membership


def create_or_update_membership(user, signup_details, complete=False):
    try:
        member = Membership.objects.get(user=user)
    except Membership.DoesNotExist:
        member = Membership()
        member.user = user

    if complete is True:
        member.status = Membership.lookup_status(name=signup_details.get('status'))
    member.email = signup_details.get('email')
    member.reference = signup_details.get('reference')
    member.payment = signup_details.get('amount')
    member.date = signup_details.get('start_date')

    member.save()

    if complete is False:
        return False  # sign up not completed

    # add user to group on success
    group = Group.objects.get(name='members')
    user.groups.add(group)
    return True  # Sign up finished
