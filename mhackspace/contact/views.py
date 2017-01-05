from django.shortcuts import render
from mhackspace.contact.forms import ContactForm

# add to your views
def contact(request):
    form_class = ContactForm
    
    return render(request, 'pages/contact.html', {
        'form': form_class,
    })
