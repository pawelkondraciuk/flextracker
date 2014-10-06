# tutorial/tables.py
import django_tables2 as tables
from issues.models import Ticket


class TicketTable(tables.Table):
    class Meta:
        model = Ticket
        exclude = ('content_type', 'object_id', 'content_object')