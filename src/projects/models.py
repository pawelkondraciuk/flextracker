from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('project_details', args=[str(self.pk)])

class Role(models.Model):
    project = models.ForeignKey(Project, related_name='roles')
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True)
    superuser = models.BooleanField(default=False)
    members = models.ManyToManyField(User)

    def __unicode__(self):
        return ' | '.join((str(self.project), self.name))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('update_role', args=[str(self.pk)])

def create_roles(sender, instance, created, **kwargs):
    if created:
        project_managers = Role.objects.create(project=instance, name='Project managers', superuser=True)
        project_managers.members.add(instance.user)
        Role.objects.create(project=instance, name='Developers')

post_save.connect(create_roles, sender=Project)