from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.contrib import messages
from mhackspace.requests.forms import UserRequestForm
from mhackspace.requests.models import UserRequests
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
            # email = EmailMessage(
            #     '[%s] - %s' % (data['enquiry_type'], data['subject']),
            #     data['message'],
            #     data['contact_email'],
            #     to=['contact@maidstone-hackspace.org.uk'],
            #     headers={'Reply-To': data['contact_email']})
            # email.send()
            messages.add_message(self.request, messages.INFO, 'Request successfully made.')

        return super(FormView, self).form_valid(form)


class RequestsList(LoginRequiredMixin, ListView):
    template_name = 'pages/requests.html'
    model = UserRequests
    context_object_name = 'requests'
    paginate_by = 5

    # def get_queryset(self):
    #     if 'category' in self.kwargs:
    #         self.category = get_object_or_404(Category, slug=self.kwargs['category'])
    #         return Post.objects.filter(active=True, categories=self.category, published_date__lte=timezone.now(), members_only=False)
    #     return Post.objects.filter(active=True, published_date__lte=timezone.now(), members_only=False)
