import re
from django import template
from django.core.urlresolvers import reverse
from django.template.base import Node, Variable
from issues.models import Ticket
from issues.tables import ShortTicketTable

register = template.Library()

mapping = ['danger', 'danger', 'primary', 'success', 'success']


@register.filter
def priority_to_bootstrap(value):
    return mapping[value - 1]


class AssignedToObjectNode(Node):
    def __init__(self, obj, var_name):
        self.obj = obj
        self.var_name = var_name

    def resolve(self, var, context):
        """Resolves a variable out of context if it's not in quotes"""
        if var[0] in ('"', "'") and var[-1] == var[0]:
            return var[1:-1]
        else:
            return Variable(var).resolve(context)

    def render(self, context):
        obj = self.resolve(self.obj, context)
        var_name = self.resolve(self.var_name, context)
        context[var_name] = Ticket.objects.assigned_to(obj)

        return ''


@register.tag
def get_assigned_to(parser, token):
    """
    Syntax::

        {% get_assigned_to obj %}
        {% for att in issues %}
            {{ att }}
        {% endfor %}

        {% get_assigned_to obj as "assigned_to_me" %}

    """

    def next_bit_for(bits, key, if_none=None):
        try:
            return bits[bits.index(key) + 1]
        except ValueError:
            return if_none

    bits = token.contents.split()
    args = {
        'obj': next_bit_for(bits, 'get_assigned_to'),
        'var_name': next_bit_for(bits, 'as', '"issues"'),
    }
    return AssignedToObjectNode(**args)

class AssignedToObjectShortTableNode(Node):
    def __init__(self, obj, var_name):
        self.obj = obj
        self.var_name = var_name

    def resolve(self, var, context):
        """Resolves a variable out of context if it's not in quotes"""
        if var[0] in ('"', "'") and var[-1] == var[0]:
            return var[1:-1]
        else:
            return Variable(var).resolve(context)

    def render(self, context):
        obj = self.resolve(self.obj, context)
        var_name = self.resolve(self.var_name, context)
        context[var_name] = ShortTicketTable(Ticket.objects.assigned_to(obj).exclude(status__type=3))

        return ''


@register.tag
def get_short_table_assigned_to(parser, token):
    """
    Syntax::

        {% get_assigned_to obj %}
        {% for att in issues %}
            {{ att }}
        {% endfor %}

        {% get_assigned_to obj as "assigned_to_me" %}

    """

    def next_bit_for(bits, key, if_none=None):
        try:
            return bits[bits.index(key) + 1]
        except ValueError:
            return if_none

    bits = token.contents.split()
    args = {
        'obj': next_bit_for(bits, 'get_short_table_assigned_to'),
        'var_name': next_bit_for(bits, 'as', '"issues"'),
    }
    return AssignedToObjectShortTableNode(**args)

def slugifier(match_object):
    val = match_object.group(1)
    return r'<a href="%s">@%s</a>' % (reverse('userena_profile_detail', args=[val]), val)

@register.filter
def url_username(text):
    return re.sub(r'(?: |^)@([\w_-]+)', slugifier, text)