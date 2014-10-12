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
    details = CustomTextLinkColumn('issue_details', kwargs={'pk': A('pk'), 'project_pk': A('object_id')}, orderable=False, empty_values=(), custom_text='View')

    class Meta:
        model = Ticket
        exclude = ('content_type', 'object_id', 'content_object')
        order_by = ('-modified',)

class MessageTable(tables.Table):
    details = CustomTextLinkColumn('issue_details', kwargs={'pk': A('pk'), 'project_pk': A('object_id')}, orderable=False, empty_values=(), custom_text='View')

    class Meta:
        model = Message
        exclude = ('content_type', 'object_id', 'content_object')
        order_by = ('-modified',)