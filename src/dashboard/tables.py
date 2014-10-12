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

class MessageTable(tables.Table):
    delete = CustomTextLinkColumn('messages_delete', kwargs={'message_id': A('pk')}, orderable=False, empty_values=(), custom_text='Delete')

    class Meta:
        model = Message
        fields = ('sender', 'subject', 'delete')