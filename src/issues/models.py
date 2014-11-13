from actstream import registry
from actstream.signals import action
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import signals
from django.db.models.deletion import SET
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.functional import SimpleLazyObject
from django_tools.middlewares import ThreadLocal
from taggit.managers import TaggableManager
from userena.mail import send_mail
from workflow.models import Status
import watson

def unique_slug(item, slug_source, slug_field):
    """Ensures a unique slug field by appending an integer counter to duplicate slugs.

    The item's slug field is first prepopulated by slugify-ing the source field. If that value already exists, a counter is appended to the slug, and the counter incremented upward until the value is unique.

    For instance, if you save an object titled Daily Roundup, and the slug daily-roundup is already taken, this function will try daily-roundup-2, daily-roundup-3, daily-roundup-4, etc, until a unique value is found.

    Call from within a model's custom save() method like so:
    unique_slug(item, slug_source='field1', slug_field='field2')
    where the value of field slug_source will be used to prepopulate the value of slug_field.
    """
    if True:  # getattr(item, slug_field): # if it's already got a slug, do nothing.
        from django.template.defaultfilters import slugify

        slug = slugify(getattr(item, slug_source))
        itemModel = item.__class__
        # the following gets all existing slug values
        allSlugs = [sl.values()[0] for sl in itemModel.objects.values(slug_field)]
        allSlugs.append(slug)
        if slug in allSlugs:
            import re

            counterFinder = re.compile(r'-\d+$')
            counter = 1
            slug = "%s-%i" % (slug, counter)
            while slug in allSlugs:
                slug = re.sub(counterFinder, "-%i" % counter, slug)
                counter += 1
        else:
            slug = "%s-1" % slug
        setattr(item, slug_field, slug)


class TicketManager(models.Manager):
    def tickets_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)

    def assigned_to(self, obj):
        return self.filter(assigned_to=obj)


PRIORITY_CHOICES = (
    (1, ('Critical')),
    (2, ('High')),
    (3, ('Normal')),
    (4, ('Low')),
    (5, ('Very Low')),
)


class Ticket(models.Model):
    slug = models.SlugField(max_length=20, unique=True, verbose_name='Code')
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    status = models.ForeignKey(Status, related_name='tickets')
    created = models.DateTimeField(auto_now_add=timezone.now)
    modified = models.DateTimeField(auto_now=timezone.now)
    submitter = models.ForeignKey(User, related_name='submitted_tickets')
    assigned_to = models.ForeignKey(User, blank=True, null=True, related_name='tickets')
    confidential = models.BooleanField()

    #
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    #tags = TaggableManager()
    objects = TicketManager()

    def __unicode__(self):
        return self.title

    @property
    def workflow(self):
        return self.content_object.workflow

    @property
    def get_code(self):
        return self.content_object.code

    def save(self, *args, **kwargs):
        if self.slug == '':
            unique_slug(self, slug_source='get_code', slug_field='slug')

        return super(Ticket, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('issue_details', args=[self.object_id, self.slug])

class TicketSearchAdapter(watson.SearchAdapter):
    fields = ('title', 'description', 'get_priority_display', 'status__name', 'submitter__username', 'slug')

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

watson.register(Ticket, TicketSearchAdapter)

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
            if type(user) is SimpleLazyObject:
                user = instance._user
            change = TicketChange.objects.create(ticket=instance, user=user)
            for key in diff:
                field = Ticket._meta.get_field(key)
                if not isinstance(field, models.ForeignKey):
                    TicketDisplayChange.objects.create(change=change, field=field.verbose_name.title(), old_value=old._get_FIELD_display(field),
                                                       new_value=instance._get_FIELD_display(field))
                else:
                    TicketDisplayChange.objects.create(change=change, field=field.verbose_name.title(), old_value=str(getattr(instance, key)),
                                                       new_value=str(getattr(instance, key)))

            if 'assigned_to' in diff:
                action.send(user, verb='assigned', action_object=instance,
                            target=instance.assigned_to)

            if 'status' in diff:
                action.send(user, verb=instance.status.verb.lower(), action_object=instance,
                            target=instance.content_object)

        #if new_instance.submitter.profile.email_notifications:
         #   send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)
#        for change_obj in change.changes:


    else:
        action.send(ThreadLocal.get_current_user(), verb='created new', action_object=instance, target=instance.content_object)



signals.pre_save.connect(apply_ticket_change, sender=Ticket)


def create_ticket(sender, instance, created, **kwargs):
    if created:
        instance.content_object.on_new_ticket(instance)


signals.post_save.connect(create_ticket, sender=Ticket)

registry.register(Ticket)