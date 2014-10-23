from django import forms
from django.core.exceptions import ValidationError
from workflow.models import Status


class StatusForm(forms.ModelForm):

    class Meta:
        model = Status

    def clean_start(self):
        start = self.cleaned_data['start']

        return start