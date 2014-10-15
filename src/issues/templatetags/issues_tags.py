from django import template

register = template.Library()

mapping = ['danger', 'danger', 'primary', 'success', 'success']


@register.filter
def priority_to_bootstrap(value):
    return mapping[value - 1]

