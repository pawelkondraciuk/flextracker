from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

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
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField()
    submitter = models.ForeignKey(User, related_name='my_tickets')
    assigned_to = models.ForeignKey(User, null=True, related_name='tickets')

    #
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    tags = TaggableManager()

class TicketChange(models.Model):
    ticket = models.ForeignKey(Ticket)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User)

class TicketDisplayChange(models.Model):
    change = models.ForeignKey(TicketChange)
    field = models.CharField(max_length=100)
    old_value = models.TextField(blank=True, null=True,)
    new_value = models.TextField(blank=True, null=True,)