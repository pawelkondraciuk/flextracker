import django_filters
from issues.models import Ticket, PRIORITY_CHOICES
from django.utils.translation import ugettext_lazy as _

class TicketFilter(django_filters.FilterSet):
    assigned_to = django_filters.CharFilter(name='assigned_to__username', label=_('Assigned to'))
    submitter = django_filters.CharFilter(name='submitter__username', label=_('Submitter'))
    created = django_filters.CharFilter(lookup_type='startswith', label=_('Created'))
    title = django_filters.CharFilter(lookup_type='icontains', label=_('Title'))
    priority = django_filters.ChoiceFilter(choices=(('', '---------'),) + PRIORITY_CHOICES, label=_('Priority'))

    class Meta:
        model = Ticket
        fields = ('title', 'priority', 'status', 'assigned_to', 'submitter', 'created', 'confidential')

    def __init__(self, *args, **kwargs):
        if 'workflow' in kwargs:
            self.workflow = kwargs.pop('workflow')
        super(TicketFilter, self).__init__(*args, **kwargs)

    @property
    def form(self):
        form = super(TicketFilter, self).form
        if hasattr(self, 'workflow'):
            form.fields['status'].queryset = self.workflow.states
        return form