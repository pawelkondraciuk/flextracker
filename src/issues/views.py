from django.views import generic
from django.views.generic.list import ListView
from django_tables2.views import SingleTableView
from issues.filters import TicketFilter
from issues.models import Ticket
from issues.tables import TicketTable
