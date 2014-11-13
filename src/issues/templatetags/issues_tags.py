import re
from django import template
from django.contrib.auth.models import User
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

class Slugifier(object):

    def __init__(self, ticket_pk):
        self.ticket = Ticket.objects.get(pk=ticket_pk)

    def slugify(self, match_object):
        user = match_object.group(1)
        ticket = match_object.group(2)
        commit = match_object.group(4)

        if user:
            if User.objects.filter(username=user).exists():
                return r' <a href="%s">@%s</a>' % (reverse('userena_profile_detail', args=[user]), user)

        if ticket:
            ticket_slug = match_object.group(3)
            if Ticket.objects.filter(slug=ticket_slug).exists():
                ticket_obj = Ticket.objects.get(slug=ticket_slug)
                return r' <a href="%s">%s</a>' % (reverse('issue_details', args=[ticket_obj.object_id, ticket_slug]), ticket)

        if commit:
            if self.ticket.content_object.github_hook:
                return r' <a href="{0}/commit/{1}">#{1}</a>'.format(self.ticket.content_object.github_hook, commit)

        return match_object.group(0)

@register.filter
def urlify(text, arg):
    slugifier = Slugifier(int(arg))
    ret = re.sub(r'(?: |^)(?:@([\w_-]+)|(\[([\w_-]+)\])|(?:#([0-9a-f]{5,40})))', slugifier.slugify, text)
    #ret = re.sub(r'(?: |^)\[([\w_-]+)\]', issue_slugifier, ret)

    return ret