from braces.views._access import PermissionRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django_tables2.views import SingleTableView

from attachments.views import set_attachments_object
from issues.forms import TicketForm
from issues.models import Ticket
from issues.tables import TicketTable
from projects.forms import RoleEditForm, RoleAddForm, ProjectAddForm
from projects.models import Project, Role
from projects.tables import ProjectTable


class ProjectListView(SingleTableView):
    template_name = 'projects/list.html'
    model = Project
    table_class = ProjectTable

    def get_queryset(self):
        return Project.objects.filter(roles__members=self.request.user)


class CreateProjectView(PermissionRequiredMixin, generic.CreateView):
    permission_required = "add_project"
    template_name = 'projects/create.html'
    model = Project
    fields = ['name',]

    def form_valid(self, form):
        project = form.save(commit=True)
        project.owner = self.request.user
        managers = project.roles.get(name='Project managers')
        managers.members.add(self.request.user)
        managers.save()

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
    template_name = 'projects/delete.html'

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
    template_name = 'issues/list.html'
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
        set_attachments_object(self.request.user, ticket, self.request.POST.getlist('files[]'))
        return super(CreateIssueView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateIssueView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('issue_details', kwargs={'pk': self.object.pk, 'project_pk': self.kwargs['pk']})

class IssueView(generic.DetailView):
    template_name = 'issues/index.html'
    model = Ticket
    context_object_name = 'issue'

    def get_context_data(self, **kwargs):
        context = super(IssueView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_pk'])
        return context

class EditIssueView(generic.UpdateView):
    template_name = 'issues/create.html'
    model = Ticket
    form_class = TicketForm
    context_object_name = 'issue'

    def get_success_url(self):
        return reverse('issue_details', kwargs={'pk': self.object.pk, 'project_pk': self.kwargs.get('project_pk')})

    def get_context_data(self, **kwargs):
        context = super(EditIssueView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_pk'])
        return context