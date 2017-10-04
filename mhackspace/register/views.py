from django.views.generic.edit import FormView
from mhackspace.register.forms import RegisteredUserForm
from mhackspace.register.models import RegisteredUser


class RegisterForm(FormView):
    template_name = 'pages/register.html'
    form_class = RegisteredUserForm
    success_url = '/register/success'

    def get(self, request, *args, **kwargs):
        name = request.POST.get('name')
        if RegisteredUser.objects.is_registered(name):
            return self.form_valid()

        if request.user.is_authenticated():
            form_kwargs = self.get_form_kwargs()
            form_kwargs['data'] = {
                'user': request.user,
                'name': request.user.name
            }
            form = self.get_form_class(**form_kwargs)
            return self.form_valid(form)

        return super(RegisterForm, self).get(self, request, *args, **kwargs)


    # Need to prevent a user registering twice
    # Need to think of a way to prevent people registering multiple times with different names

