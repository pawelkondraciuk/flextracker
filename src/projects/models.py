from actstream.actions import follow, unfollow
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from actstream import action, registry

from issues.models import Ticket


class Role(models.Model):
    project = models.ForeignKey('Project', related_name='roles')
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True)
    superuser = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='roles')

    def __unicode__(self):
        return ' | '.join((str(self.project), self.name))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('update_role', args=[str(self.pk)])

class Project(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    members = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)

    tickets = generic.GenericRelation(Ticket)

    def __unicode__(self):
        return self.name

    def delete(self, using=None):
        self.members.delete()
        return super(Project, self).delete(using)

    def save(self, *args, **kwargs):
        if self.pk is None:
            ret = super(Project, self).save(*args, **kwargs)
            Role.objects.create(project=self, name='Developers')
            Role.objects.create(project=self, name='Project managers', superuser=True)
            self.members = Group.objects.create(name='%s_%d' % (self.name, self.pk))
            return ret

        return super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('project_details', args=[str(self.pk)])

    def on_new_ticket(self, ticket):
        action.send(ticket.submitter, verb='created new ticket', action_object=ticket, target=self)


def modify_project_group(sender, instance, **kwargs):
    if instance.pk:
        a = User.objects.filter(groups=instance.project.members)
        b = User.objects.filter(roles__project=instance.project)
        to_remove = a.exclude(id__in=b)
        to_add = b.exclude(id__in=a)
        for user in to_remove:
            unfollow(user, instance)
        for user in to_add:
            follow(user, instance)
        instance.project.members.user_set.add(*to_add)
        instance.project.members.user_set.remove(*to_remove)


pre_save.connect(modify_project_group, sender=Role)

registry.register(Role)
registry.register(Group)
registry.register(User)