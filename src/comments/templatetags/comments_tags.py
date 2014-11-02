import re
from django.template import Library, Node, Variable
from comments.forms import CommentForm
from comments.models import Comment

register = Library()


@register.inclusion_tag('comments/add_form.html', takes_context=True)
def comment_form(context, obj):
    """
    Renders a "upload attachment" form.
    
    The user must own ``attachments.add_attachment permission`` to add
    attachments.
    """
    if context['user'].has_perm('attachments.add_attachment'):
        return {
            'form': CommentForm(),
            'next': context['request'].build_absolute_uri(),
        }
    else:
        return {
            'form': None,
        }


class CommentsForObjectNode(Node):
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
        context[var_name] = Comment.objects.comments_for_object(obj)
        return ''


@register.tag
def get_comments_for(parser, token):
    def next_bit_for(bits, key, if_none=None):
        try:
            return bits[bits.index(key) + 1]
        except ValueError:
            return if_none

    bits = token.contents.split()
    args = {
        'obj': next_bit_for(bits, 'get_comments_for'),
        'var_name': next_bit_for(bits, 'as', '"comments"'),
    }
    return CommentsForObjectNode(**args)