from django import forms
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from issues.models import Ticket
from projects.models import Role, Project
from workflow.models import Workflow

class WorkflowRadioChoiceInput(forms.widgets.RadioChoiceInput):

    def __init__(self, *args, **kwargs):
        super(WorkflowRadioChoiceInput, self).__init__(*args, **kwargs)

        self.choice_label = force_text(format_html('{0} <a href="{1}">Edit</a>', force_text(args[3][1]), force_text(reverse('update_workflow', args=[args[3][0]]))))


class WorkflowRadioFieldRenderer(forms.widgets.RadioFieldRenderer):
    choice_input_class = WorkflowRadioChoiceInput

class WorkflowRadioSelect(forms.RadioSelect):
    renderer = WorkflowRadioFieldRenderer

class RoleEditForm(forms.ModelForm):
    class Meta:
        model = Role
        exclude = ('project',)

    def __init__(self, *args, **kwargs):
        super(RoleEditForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.filter(content_type__model__in=['ticket', 'attachment', 'role', 'project'])

class RoleAddForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ('name',)

class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'code', 'workflow')
        widgets = {
            'workflow': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateProjectForm, self).__init__(*args, **kwargs)
        self.fields['workflow'].queryset = Workflow.objects.workflow_for_object(self.instance)
        self.fields['workflow'].empty_label = None