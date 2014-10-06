from django import forms
from issues.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('created', 'modified', 'submitter', 'content_type', 'object_id', 'content_object')