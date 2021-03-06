# tutorial/tables.py
from django_messages.models import Message
import django_tables2 as tables
from django_tables2.utils import A, Accessor
from issues.models import Ticket
from django.utils.translation import ugettext_lazy as _

class CustomTextURLColumn(tables.URLColumn):
    def __init__(self, custom_text=None, *args, **kwargs):
        super(CustomTextLinkColumn, self).__init__(*args, **kwargs)
        self.custom_text = custom_text


    def render(self, value, record, bound_column):
        return self.render_link.render(self.custom_text if self.custom_text else value, value)

class CustomTextLinkColumn(tables.LinkColumn):
    def __init__(self, viewname, urlconf=None, args=None,
                 kwargs=None, current_app=None, attrs=None, custom_text=None, **extra):
        super(CustomTextLinkColumn, self).__init__(viewname, urlconf=urlconf,
                                                   args=args, kwargs=kwargs, current_app=current_app, attrs=attrs,
                                                   **extra)
        self.custom_text = custom_text


    def render(self, value, record, bound_column):
        return super(CustomTextLinkColumn, self).render(
            self.custom_text if self.custom_text else value,
            record, bound_column)


class MessageTable(tables.Table):
    delete = CustomTextLinkColumn('messages_delete', kwargs={'message_id': A('pk')}, orderable=False, empty_values=(),
                                  custom_text=_('Delete'))
    subject = tables.LinkColumn('messages_detail', args=[A('id'),], verbose_name=_('Subject'))

    class Meta:
        model = Message
        fields = ('subject', 'sender', 'delete')