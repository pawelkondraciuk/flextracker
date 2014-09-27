from braces.views._access import PermissionRequiredMixin
from django.shortcuts import render
from django.views import generic
from projects.models import Project

class ProjectListView(generic.ListView):
    template_name = 'projects/list.html'
    model = Project
    context_object_name = 'projects'
    queryset = Project.objects.all()

class CreateProjectView(PermissionRequiredMixin, generic.CreateView):
    permission_required = "add_project"
    template_name = 'projects/create.html'
    model = Project
    fields = ['name',]

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user

        return super(CreateProjectView, self).form_valid(form)

class ProjectDetailsView(generic.DetailView):
    template_name = 'projects/details.html'
    model = Project
    context_object_name = 'project'

class EditProjectView(generic.UpdateView):
    template_name = 'projects/edit.html'
    model = Project