from django import forms

TYPES = (
    ('general', 'General'),
    ('donate', 'Donate equipment money or time'),
    ('event', 'Event')
)

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
    type = forms.MultipleChoiceField(
        required=True,
        widget=forms.Select,
        choices=TYPES)
