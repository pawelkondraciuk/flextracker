from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
from django.views import generic
from workflow.models import Workflow


class UpdateWorkflow(generic.UpdateView):
    template_name = 'workflow/create.html'
    model = Workflow
    context_object_name = 'workflow'


class CreateWorkflow(generic.CreateView):
    template_name = 'workflow/create.html'
    model = Workflow
    

class DeleteWorkflow(generic.DeleteView):
    model = Workflow
    template_name = 'workflow/delete.html'
    success_url = '#'