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

class Status(models.Model):
    name = models.CharField(max_length=50)
    available_states = models.ManyToManyField('self', blank=True)
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    workflow = models.ForeignKey('Workflow', related_name='states')

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
            Status.objects.create(name='Open', type=1, workflow=self)
            Status.objects.create(name='Closed', type=3, workflow=self)

        return ret

    def __unicode__(self):
        return self.name


    @property
    def start_state(self):
        return self.states.get(type=1)


    @property
    def end_state(self):
        return self.states.get(type=3)