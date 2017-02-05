from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib import messages
from mhackspace.contact.forms import ContactForm

# add to your views
def contact(request):
    form_class = ContactForm
    form = form_class(data=request.POST)
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = EmailMessage(
                '[%s] - %s' % (data['enquiry_type'], data['subject']),
                data['message'],
                to=['no-reply@maidstone-hackspace..org.uk'])
            email.send()
            messages.add_message(request, messages.INFO, 'E-Mail sent')


    return render(request, 'pages/contact.html', {
        'form': form,
    })

