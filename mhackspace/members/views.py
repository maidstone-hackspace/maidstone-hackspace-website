# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from mhackspace.users.models import User


class MemberListView(LoginRequiredMixin, ListView):
    template_name = "pages/members.html"
    queryset = User.objects.prefetch_related("user", "groups")
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        if self.kwargs.get("status") == "registered":
            context["members"] = self.get_queryset().filter(
                groups__name="members"
            )
        else:
            context["members"] = self.get_queryset()
        context["total_users"] = self.get_queryset().count()
        context["total_members"] = (
            self.get_queryset().filter(groups__name="members").count()
        )
        return context
