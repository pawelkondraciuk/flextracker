# tutorial/tables.py
from django_messages.models import Message
import django_tables2 as tables
from django_tables2.utils import A, Accessor
from issues.models import Ticket

class CustomTextLinkColumn(tables.LinkColumn):
  def __init__(self, viewname, urlconf=None, args=None,
    kwargs=None, current_app=None, attrs=None, custom_text=None, **extra):
    super(CustomTextLinkColumn, self).__init__(viewname, urlconf=urlconf,
      args=args, kwargs=kwargs, current_app=current_app, attrs=attrs, **extra)
    self.custom_text = custom_text


  def render(self, value, record, bound_column):
    return super(CustomTextLinkColumn, self).render(
      self.custom_text if self.custom_text else value,
      record, bound_column)

class TicketTable(tables.Table):
    slug = tables.LinkColumn('issue_details', kwargs={'slug': A('slug'), 'project_pk': A('object_id')})
    submitter = tables.LinkColumn('userena_profile_detail', args=[A('submitter.username')])
    assigned_to = tables.LinkColumn('userena_profile_detail', args=[A('assigned_to.username')])

    class Meta:
        model = Ticket
        exclude = ('id', 'content_type', 'object_id', 'content_object', 'description')
        order_by = ('-modified',)

class ShortTicketTable(tables.Table):
    slug = tables.LinkColumn('issue_details', kwargs={'slug': A('slug'), 'project_pk': A('object_id')})

    class Meta:
        model = Ticket
        fields = ('slug', 'title', 'priority', 'status')
        order_by = ('-modified',)

class MessageTable(tables.Table):
    details = CustomTextLinkColumn('issue_details', kwargs={'slug': A('slug'), 'project_pk': A('object_id')}, orderable=False, empty_values=(), custom_text='View')

    class Meta:
        model = Message
        exclude = ('content_type', 'object_id', 'content_object')
        order_by = ('-modified',)