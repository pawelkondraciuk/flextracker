from django.views import generic
from django.views.generic.list import ListView
from issues.models import Ticket


class IssueListView(ListView):
    template_name = 'issues/index.html'
    context_object_name = 'issues'
    model = Ticket
    queryset = Ticket.objects.all()

class CreateIssueView(generic.CreateView):
    model = Ticket
    fields = ['description',]