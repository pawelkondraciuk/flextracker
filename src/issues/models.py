from actstream import registry
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import signals
from django.forms.models import model_to_dict
from django.utils import timezone
from django_tools.middlewares import ThreadLocal
from taggit.managers import TaggableManager


class TicketManager(models.Manager):
    def tickets_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)

PRIORITY_CHOICES = (
    (1, ('Critical')),
    (2, ('High')),
    (3, ('Normal')),
    (4, ('Low')),
    (5, ('Very Low')),
)

class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    created = models.DateTimeField(auto_now_add=timezone.now)
    modified = models.DateTimeField(auto_now=timezone.now)
    submitter = models.ForeignKey(User, related_name='submitted_tickets')
    assigned_to = models.ForeignKey(User, blank=True, null=True, related_name='tickets')

    #
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    tags = TaggableManager()
    objects = TicketManager()

class TicketChange(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='changes')
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User)

class TicketDisplayChange(models.Model):
    change = models.ForeignKey(TicketChange, related_name='details')
    field = models.CharField(max_length=100)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)


def _as_dict(obj):
    return dict([(f.name, getattr(obj, f.name)) for f in obj._meta.local_fields if not f.rel])


def apply_ticket_change(sender, instance, **kwargs):
    if instance.pk:
        old = instance.__class__.objects.get(pk=instance.pk)
        old_instance = model_to_dict(old, fields=[field.name for field in old._meta.fields])
        new_instance = model_to_dict(instance, fields=[field.name for field in instance._meta.fields])
        diff = [key for key, value in old_instance.items() if value != new_instance[key]]
        if diff:
            user = ThreadLocal.get_current_user()
            change = TicketChange.objects.create(ticket=instance, user=user)
            for key in diff:
                TicketDisplayChange.objects.create(change=change, field=key, old_value=str(getattr(old, key)),
                                                   new_value=str(getattr(instance, key)))

            if 'assigned_to' in diff:
                assigned_to = instance.assigned_to


signals.pre_save.connect(apply_ticket_change, sender=Ticket)


def create_ticket(sender, instance, created, **kwargs):
    if created:
        instance.content_object.on_new_ticket(instance)


signals.post_save.connect(create_ticket, sender=Ticket)

registry.register(Ticket)

#
#
# class Workflow(models.Model):
# pass
#
# class Status(models.Model):
#     name = models.CharField(max_length=50)
#     available_states = models.ManyToManyField('self')
#