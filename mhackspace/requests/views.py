from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from mhackspace.requests.forms import UserRequestForm, UserRequestFormComment
from mhackspace.requests.models import UserRequest, UserRequestsComment
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse


class RequestsForm(LoginRequiredMixin, FormView):
    template_name = 'pages/requests.html'
    form_class = UserRequestForm
    success_url = '/requests/'

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            messages.add_message(self.request, messages.INFO, 'Request successfully made.')
        return super(FormView, self).form_valid(form)


class RequestsDetailForm(LoginRequiredMixin, FormView):
    template_name = 'pages/requests-detail.html'
    form_class = UserRequestFormComment

    def get_success_url(self):
        return reverse(
            'requests_detail',
            kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.request_id = self.kwargs.get('pk')
            obj.save()
        messages.add_message(self.request, messages.INFO, 'Request comment added.')
        return super(FormView, self).form_valid(form)


class RequestsDetail(LoginRequiredMixin, DetailView):
    model = UserRequest
    context_object_name = 'request_detail'

    def get_context_data(self, *args, **kwargs):
        context = super(RequestsDetail, self).get_context_data(*args, **kwargs)
        context['requests_comments'] = UserRequestsComment.objects.all()
        context['form'] = UserRequestFormComment
        return context


class RequestsList(LoginRequiredMixin, ListView):
    template_name = 'pages/requests.html'
    model = UserRequest
    context_object_name = 'requests'
    paginate_by = 50


    def get_queryset(self):
        new_context = UserRequest.objects.filter(
            acquired=False,
        )
        return new_context

    def get_context_data(self, *args, **kwargs):
        context = super(RequestsList, self).get_context_data(*args, **kwargs)
        context['requests_history'] = UserRequest.objects.filter(acquired=True)[:50]
        return context
