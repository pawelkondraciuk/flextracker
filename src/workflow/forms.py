from django import forms
from django.core.exceptions import ValidationError
from workflow.models import Status


class StatusForm(forms.ModelForm):

    class Meta:
        model = Status


    def clean_start(self):
        start = self.cleaned_data['start']

        return start

class MappingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        from_workflow = kwargs.pop('from_workflow')
        to_workflow = kwargs.pop('to_workflow')
        for state in from_workflow.states.all():
            self.base_fields[str(state.id)] = forms.ModelChoiceField(queryset=to_workflow.states, label=state.name)

        super(MappingForm, self).__init__(*args, **kwargs)
