from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.contrib import messages
from mhackspace.requests.forms import UserRequestForm
from mhackspace.requests.models import UserRequest
from django.views.generic import ListView
from django.views.generic.edit import FormView


class RequestsForm(LoginRequiredMixin, FormView):
    template_name = 'pages/requests.html'
    form_class = UserRequestForm
    success_url = '/requests'

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            messages.add_message(self.request, messages.INFO, 'Request successfully made.')
        return super(FormView, self).form_valid(form)


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
