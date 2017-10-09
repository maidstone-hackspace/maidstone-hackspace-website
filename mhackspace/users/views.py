# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Rfid
from .models import User
from .models import Blurb
from .models import Membership

from .forms import BlurbForm, MembershipJoinForm

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['blurb'] = Blurb.objects.filter(user=self.get_object()).first()
        context['membership'] = Membership.objects.filter(user=self.get_object()).first()
        context['membership_form'] = MembershipJoinForm(initial={'amount': 20.00})
        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name', '_image', ]
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse(
            'users:detail',
            kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        profile = Blurb.objects.filter(user=self.get_object()).first()
        context['form_blurb'] = BlurbForm(instance=profile)
        return context

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        profile = Blurb.objects.filter(user=self.get_object()).first()
        form_blurb = BlurbForm(self.request.POST, instance=profile)
        if form_blurb.is_valid():
            blurb_model = form_blurb.save(commit=False)
            blurb_model.user = self.request.user
            blurb_model.save()

        return super(UserUpdateView, self).form_valid(form)


class RfidCardsUpdateView(LoginRequiredMixin, CreateView):
    fields = ['user', 'code', 'description', ]
    model = Rfid

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(RfidCardsUpdateView, self).form_valid(form)



class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
