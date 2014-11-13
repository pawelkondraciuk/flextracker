import django_filters
from issues.models import Ticket, PRIORITY_CHOICES


class TicketFilter(django_filters.FilterSet):
    assigned_to = django_filters.CharFilter(name='assigned_to__username')
    submitter = django_filters.CharFilter(name='submitter__username')
    created = django_filters.CharFilter(lookup_type='startswith')
    title = django_filters.CharFilter(lookup_type='icontains')
    priority = django_filters.ChoiceFilter(choices=(('', '---------'),) + PRIORITY_CHOICES)

    class Meta:
        model = Ticket
        fields = ('title', 'priority', 'status', 'assigned_to', 'submitter', 'created', 'confidential')

    def __init__(self, workflow, *args, **kwargs):
        super(TicketFilter, self).__init__(*args, **kwargs)
        self.workflow = workflow

    @property
    def form(self):
        form = super(TicketFilter, self).form
        form.fields['status'].queryset = self.workflow.states
        return form