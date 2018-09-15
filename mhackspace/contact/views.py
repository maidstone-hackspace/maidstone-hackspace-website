from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib import messages
from mhackspace.contact.forms import ContactForm


def contact(request):
    form_class = ContactForm
    if request.method == "POST":
        form = form_class(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = EmailMessage(
                "[%s] - %s" % (data["enquiry_type"], data["subject"]),
                data["message"],
                data["contact_email"],
                to=["contact@maidstone-hackspace.org.uk"],
                headers={"Reply-To": data["contact_email"]},
            )
            email.send()
            messages.add_message(request, messages.INFO, "E-Mail sent")
    else:
        form = form_class()

    return render(
        request,
        "pages/contact.html",
        {"form": form, "open_graph": {"title": "Contact Us", "type": "article"}},
    )
