from django.views import generic
from django.views.generic.list import ListView
from django_tables2.views import SingleTableView
from issues.filters import TicketFilter
from issues.models import Ticket
from issues.tables import TicketTable


class IssueListView(SingleTableView):
    template_name = 'issues/list.html'
    table_class = TicketTable

    def get_qs(self):
        return project.tickets.filter(Q(confidential=False) | Q(confidential=True, submitter=self.request.user)).all()

    def get_queryset(self):
        return TicketFilter(self.request.GET, queryset=self.get_qs())