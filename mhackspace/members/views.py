# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from mhackspace.users.models import User

class MemberListView(LoginRequiredMixin, ListView):
    template_name = 'pages/members.html'
    queryset = User.objects.prefetch_related('user', 'groups')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        context['members'] = self.get_queryset()
        context['total'] = self.get_queryset().filter(groups__name='members').count()
        return context
