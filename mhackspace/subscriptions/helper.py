# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import logging
from datetime import datetime
from django.contrib.auth.models import Group
from django.utils.dateparse import parse_datetime
from mhackspace.users.models import Membership
from mhackspace.users.models import MEMBERSHIP_CANCELLED, MEMBERSHIP_ACTIVE

logger = logging.getLogger(__name__)


def create_or_update_membership(user, signup_details, complete=False):
    start_date = signup_details.get('start_date')
    if not isinstance(start_date, datetime):
        start_date = parse_datetime(start_date)
    try:
        member = Membership.objects.get(email=signup_details.get('email'))
        # Only update if newer than last record, this way we only get the latest status
        # cancellation and changed payment will not be counted against current status
        if start_date < member.date:
            return True
    except Membership.DoesNotExist:
        member = Membership()
        member.user = user

    if complete is True:
        member.status = MEMBERSHIP_ACTIVE
    member.email = signup_details.get('email')
    member.reference = signup_details.get('reference')
    member.payment = signup_details.get('amount')
    member.date = start_date

    member.save()

    if complete is False:
        return False  # sign up not completed

    # add user to group on success

    if user:
        try:
            group = Group.objects.get(name='members')
            user.groups.add(group)
        except:
            logger.error('Members group does not exist')
    return True  # Sign up finished


def cancel_membership(user):
    member = Membership.objects.get(user=user)
    member.status = MEMBERSHIP_CANCELLED
    member.save()

    group = Group.objects.get(name='members')
    user.groups.remove(group)
    return True
