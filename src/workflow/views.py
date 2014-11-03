from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render

# Create your views here.
from django.views import generic
from workflow.forms import MappingForm
from workflow.models import Workflow


class UpdateWorkflow(generic.UpdateView):
    template_name = 'workflow/edit.html'
    model = Workflow
    context_object_name = 'workflow'


class CreateWorkflow(generic.CreateView):
    template_name = 'workflow/create.html'
    model = Workflow
    

class DeleteWorkflow(generic.DeleteView):
    model = Workflow
    template_name = 'workflow/delete.html'
    success_url = '#'

class WorkflowMapping(generic.FormView):
    template_name = 'workflow/mapping.html'
    form_class = MappingForm

    def get_form(self, form_class):
        from_workflow = Workflow.objects.get(pk=self.kwargs.get('from'))
        to_workflow = Workflow.objects.get(pk=self.kwargs.get('to'))
        return form_class(from_workflow=from_workflow, to_workflow=to_workflow, **self.get_form_kwargs())

    def form_valid(self, form):
        from_workflow = Workflow.objects.get(pk=self.kwargs.get('from'))
        to_workflow = Workflow.objects.get(pk=self.kwargs.get('to'))

        with transaction.atomic():
            from_workflow.content_object.workflow = to_workflow
            from_workflow.content_object.save()

            for state in from_workflow.states.all():
                state.tickets.update(status=form.cleaned_data[str(state.id)])
                state.save()

        return super(WorkflowMapping, self).form_valid(form)

    def get_success_url(self):
        to_workflow = Workflow.objects.get(pk=self.kwargs.get('to'))
        return to_workflow.content_object.get_absolute_url()