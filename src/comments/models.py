import re
import actstream
from actstream import registry
from actstream.signals import action
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
import watson
from django.utils.translation import ugettext_lazy as _


class CommentManager(models.Manager):
    def comments_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)

class Comment(models.Model):
    objects = CommentManager()

    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name=_('Comment'))
    author = models.ForeignKey(User)
    #
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def get_absolute_url(self):
        return "%s#%s" % (self.content_object.get_absolute_url(), self.pk)

    def __unicode__(self):
        if len(self.content) < 50:
            return self.content + '...'
        else:
            return self.content[50:] + '...'

class CommentSearchAdapter(watson.SearchAdapter):
    fields = ('content', 'author')

    def get_title(self, obj):
        return obj.content_object.title

    def get_description(self, obj):
        return obj.content

watson.register(Comment, CommentSearchAdapter)

registry.register(Comment)

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, created, instance, **kwargs):
    if created:
        iter = set(re.findall("(?: |^)@([\w_-]+)", instance.content))
        for i in iter:
            try:
                user_found = User.objects.get(username=i)
                if user_found != instance.author:
                    action.send(instance.author, recipient=user_found, verb='used your name', action_object=instance, target=instance.content_object)
            except User.DoesNotExist:
                pass