from actstream.signals import action

from braces.views._access import PermissionRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.forms.widgets import RadioSelect
from django.views import generic
from django_tables2.views import SingleTableView

from attachments.views import set_attachments_object
from issues.filters import TicketFilter
from issues.forms import TicketForm, CreateTicketForm
from issues.models import Ticket
from issues.tables import TicketTable
from projects.forms import RoleEditForm, RoleAddForm, UpdateProjectForm
from projects.models import Project, Role
from projects.tables import ProjectTable
from workflow.models import Workflow


class ProjectListView(SingleTableView):
    template_name = 'projects/list.html'
    model = Project
    table_class = ProjectTable
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(Q(roles__members=self.request.user, private=True) | Q(private=False)).distinct()


class CreateProjectView(PermissionRequiredMixin, generic.CreateView):
    permission_required = "add_project"
    template_name = 'projects/create.html'
    model = Project
    fields = ('name', 'code', 'workflow')

    def get_form(self, form_class):
        form = super(CreateProjectView, self).get_form(form_class)
        form.fields['workflow'].queryset = Workflow.objects.none()
        form.fields['workflow'].widget = RadioSelect()
        form.fields['workflow'].label = 'Workflow <i class="fa fa-plus"></i>'

        return form

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
    form_class = UpdateProjectForm

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

    def get_qs(self):
        project = Project.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user in project.members.user_set.all():
            return project.tickets.all()
        return project.tickets.filter(Q(confidential=False) | Q(confidential=True, submitter=self.request.user)).all()

    def get_queryset(self):
        return TicketFilter(self.request.GET, queryset=self.get_qs())

    def get_context_data(self, **kwargs):
        context = super(IssueListView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context

class GlobalIssueListView(SingleTableView):
    template_name = 'issues/list.html'
    table_class = TicketTable

    def get_qs(self):
        qs = QuerySet(model=Ticket)

        for project in Project.objects.filter(roles__members=self.request.user):
            qs |= project.tickets.all()

        for project in Project.objects.exclude(roles__members=self.request.user):
            qs |= project.tickets.filter(confidential=False)

        return qs
        #return Ticket..filter(Q(confidential=False) | Q(confidential=True, submitter=self.request.user)).all()

    def get_queryset(self):
        return TicketFilter(self.request.GET, queryset=self.get_qs())

class CreateIssueView(generic.CreateView):
    template_name = 'issues/create.html'
    form_class = CreateTicketForm

    def get_form(self, form_class):
        return form_class(Project.objects.get(pk=self.kwargs['pk']).workflow, **self.get_form_kwargs())

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
        return reverse('issue_details', kwargs={'slug': self.object.slug, 'project_pk': self.kwargs['pk']})


class IssueView(UserPassesTestMixin, generic.DetailView):
    template_name = 'issues/index.html'
    model = Ticket
    context_object_name = 'issue'

    def test_func(self, user):
        issue = self.get_object()
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        return not issue.confidential or (issue.confidential and (user == issue.submitter or project.roles.filter(members=user).exists()))

    def get_context_data(self, **kwargs):
        context = super(IssueView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_pk'])
        return context


class EditIssueView(generic.UpdateView):
    template_name = 'issues/create.html'
    model = Ticket
    form_class = TicketForm
    context_object_name = 'issue'

    def form_valid(self, form):
        ticket = form.save(commit=False)
        set_attachments_object(self.request.user, ticket, self.request.POST.getlist('files[]'))
        return super(EditIssueView, self).form_valid(form)

    def get_form(self, form_class):
        return form_class(Project.objects.get(pk=self.kwargs['project_pk']).workflow, **self.get_form_kwargs())

    def get_success_url(self):
        return reverse('issue_details', kwargs={'slug': self.object.slug, 'project_pk': self.kwargs.get('project_pk')})

    def get_context_data(self, **kwargs):
        context = super(EditIssueView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_pk'])
        return context