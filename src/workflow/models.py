from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


class WorkflowManager(models.Manager):
    def workflow_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)


TYPE_CHOICES = (
    (1, 'Start'),
    (2, 'Middle'),
    (3, 'Last')
)


class ReadNestedWriteFlatMixin(object):
    """
    Mixin that sets the depth of the serializer to 0 (flat) for writing operations.
    For all other operations it keeps the depth specified in the serializer_class
    """

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = super(ReadNestedWriteFlatMixin, self).get_serializer_class(*args, **kwargs)
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            serializer_class.Meta.depth = 0
        return serializer_class


class Status(ReadNestedWriteFlatMixin, models.Model):
    name = models.CharField(max_length=50)
    available_states = models.ManyToManyField('self', blank=True, symmetrical=False)
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    verb = models.CharField(max_length=50)
    workflow = models.ForeignKey('Workflow', related_name='states', null=True, blank=True)

    class Meta:
        verbose_name = 'Statu'

    def __unicode__(self):
        return self.name


class Workflow(models.Model):
    name = models.CharField(max_length=50)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = WorkflowManager()

    def save(self, *args, **kwargs):
        pk = self.pk

        ret = super(Workflow, self).save(*args, **kwargs)

        if pk is None:
            open = Status.objects.create(name='Open', type=1, workflow=self)
            closed = Status.objects.create(name='Closed', type=3, workflow=self)
            open.available_states = [closed]
            open.save()
            closed.save()

        return ret

    def __unicode__(self):
        return self.name


    @property
    def start_state(self):
        return self.states.get(type=1)


    @property
    def end_state(self):
        return self.states.get(type=3)