from django import forms
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from attachments.models import Attachment
from comments.models import Comment
from workflow.models import Status


class CommentForm(ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3}))
    status = forms.ModelChoiceField(required=False, queryset=Status.objects.none(), widget=forms.RadioSelect())

    class Meta:
        model = Comment
        fields = ['content', 'status']

    def set_statuses(self, qs):
        if qs.count() == 0:
            self.fields.pop('status')
        else:
            self.fields['status'].queryset = qs