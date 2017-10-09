from django.views.generic.edit import FormView

from mhackspace.register.forms import RegisteredUserForm
from mhackspace.register.models import RegisteredUser


class RegisterForm(FormView):
    template_name = 'pages/register.html'
    form_class = RegisteredUserForm
    success_url = '/register/success'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if not RegisteredUser.objects.is_registered(request.user):
                registered_user = RegisteredUser.objects.create(user=request.user, name=request.user.username)
                registered_user.save()
            return super(RegisterForm, self).form_valid(None)

        return super(RegisterForm, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            form.save()

        return super(RegisterForm, self).form_valid(form)
