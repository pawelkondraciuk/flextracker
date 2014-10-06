from braces.views._access import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.sitemaps.tests.urls.http import generic_sitemaps
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.views import generic
from django_tables2.views import SingleTableMixin, SingleTableView
from issues.forms import TicketForm
from issues.tables import TicketTable
from projects.forms import RoleEditForm, RoleAddForm, ProjectAddForm
from projects.models import Project, Role


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
        project = form.save(commit=True)
        project.owner = self.request.user
        project.roles.get(name='Project managers').members.add(self.request.user)

        return super(CreateProjectView, self).form_valid(form)

class ProjectDetailsView(generic.DetailView):
    template_name = 'projects/details.html'
    context_object_name = 'project'
    model = Project

class EditProjectView(generic.UpdateView):
    template_name = 'projects/edit.html'
    model = Project
    form_class = ProjectAddForm

    def form_valid(self, form):
        if not isinstance(form, self.get_form_class()):
            form.instance.project = self.get_object()

        return super(EditProjectView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditProjectView, self).get_context_data(**kwargs)
        context['role_form'] = RoleAddForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'form' in request.POST:
            return super(EditProjectView, self).post(request, *args, **kwargs)

        form_class = RoleAddForm
        form_name = 'role_form'

        self.object = self.get_object()

        form = form_class(self.request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

class DeleteProjectView(generic.DeleteView, UserPassesTestMixin):
    model = Project
    success_url = reverse_lazy('projects')

    def test_func(self, user):
        return True

class RoleEditView(generic.UpdateView):
    template_name = 'projects/role_edit.html'
    form_class = RoleEditForm
    model = Role

    def get_context_data(self, **kwargs):
        context = super(RoleEditView, self).get_context_data(**kwargs)
        context['project'] = Role.objects.get(pk=self.kwargs['pk']).project
        return context
    
    def get_success_url(self):
        return reverse('update_project', args=[Role.objects.get(pk=self.kwargs['pk']).project.pk])

class RoleDeleteView(generic.DeleteView):
    model = Role

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('update_project', args=[Role.objects.get(pk=self.kwargs['pk']).project.pk])

class IssueListView(SingleTableView):
    template_name = 'issues/index.html'
    table_class = TicketTable

    def get_queryset(self):
        return Project.objects.get(pk=self.kwargs.get('pk')).tickets.all()

    def get_context_data(self, **kwargs):
        context = super(IssueListView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context

class CreateIssueView(generic.CreateView):
    template_name = 'issues/create.html'
    form_class = TicketForm

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.content_object = Project.objects.get(pk=self.kwargs['pk'])
        ticket.submitter = self.request.user
        ticket.save()
        return super(CreateIssueView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateIssueView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context