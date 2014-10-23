from django import template
from django.template.base import Node, Variable
from dashboard.tables import MessageTable

register = template.Library()

class MessageTableNode(Node):
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
        context[var_name] = MessageTable(obj)

        return ''


@register.tag
def get_message_table_for(parser, token):
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
        'obj': next_bit_for(bits, 'get_message_table_for'),
        'var_name': next_bit_for(bits, 'as', '"messages"'),
    }
    return MessageTableNode(**args)