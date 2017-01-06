# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .models import UserBlurb
from .models import UserMembership

from .forms import UserBlurbForm

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['blurb'] = UserBlurb.objects.filter(user=self.get_object()).first()
        context['membership'] = UserMembership.objects.filter(user=self.get_object()).first()
        return context

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name', 'image', ]
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse(
            'users:detail',
            kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        profile = UserBlurb.objects.filter(user=self.get_object()).first()
        context['form_blurb'] = UserBlurbForm(instance=profile)
        return context

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        profile = UserBlurb.objects.filter(user=self.get_object()).first()
        form_blurb = UserBlurbForm(self.request.POST, instance=profile)
        if form_blurb.is_valid():
            blurb_model = form_blurb.save(commit=False)
            blurb_model.user = self.request.user
            blurb_model.save()

        return super(UserUpdateView, self).form_valid(form)

class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
