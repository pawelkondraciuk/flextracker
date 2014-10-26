import django_filters
from issues.models import Ticket


class TicketFilter(django_filters.FilterSet):
    assigned_to = django_filters.CharFilter(name='assigned_to__username')
    submitter = django_filters.CharFilter(name='submitter__username')
    created = django_filters.CharFilter(lookup_type='startswith')

    class Meta:
        model = Ticket
