from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

class WorkflowManager(models.Manager):
    def workflow_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)

class Status(models.Model):
    name = models.CharField(max_length=50)
    available_states = models.ManyToManyField('self', blank=True)
    start = models.BooleanField(default=False)
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
            Status.objects.create(name='Start', start=True, workflow=self)

        return ret

    def __unicode__(self):
        return self.name