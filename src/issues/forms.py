from django import forms
from issues.models import Ticket
from workflow.models import Status


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('created', 'modified', 'submitter', 'content_type', 'object_id', 'content_object', 'slug')

    def __init__(self, workflow, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = (self.instance.status.available_states.all() | Status.objects.filter(pk=self.instance.status.pk)).distinct()


    def save(self, commit=True):
        obj = super(TicketForm, self).save(commit=False)

        if commit:
            obj.save()

        return obj

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('created', 'modified', 'submitter', 'content_type', 'object_id', 'content_object', 'status', 'slug', 'assigned_to')

    def __init__(self, workflow, *args, **kwargs):
        super(CreateTicketForm, self).__init__(*args, **kwargs)
        self.workflow = workflow

    def save(self, commit=True):
        obj = super(CreateTicketForm, self).save(commit=False)
        obj.status = self.workflow.states.get(type=1)
        if commit:
            obj.save()

        return obj