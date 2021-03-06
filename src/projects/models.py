from actstream.actions import follow, unfollow
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from actstream import action, registry
import watson

from issues.models import Ticket
from workflow.models import Workflow
from github_hook.models import hook_signal
from django.utils.translation import ugettext_lazy as _

class Role(models.Model):
    project = models.ForeignKey('Project', related_name='roles', verbose_name=_('Project'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name=_('Permissions'))
    superuser = models.BooleanField(default=False, verbose_name=_('Superuser'))
    members = models.ManyToManyField(User, related_name='roles', blank=True, verbose_name=_('Members'))

    def __unicode__(self):
        return u' | '.join((str(self.project), self.name))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('update_role', args=[str(self.pk)])

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=5, unique=True, help_text=_('Used to generate ticket slugs'), verbose_name=_('Code'))
    created = models.DateTimeField(default=timezone.now, verbose_name=_('Created'))
    members = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, verbose_name=_('Members'))
    workflow = models.ForeignKey(Workflow, verbose_name=_('Workflow'))
    private = models.BooleanField(default=False, verbose_name=_('Private'))

    github_hook = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name=_('GitHub repository address'), help_text=_('Please add http://localhost:8000/hook to your GitHub webhooks.'))

    tickets = generic.GenericRelation(Ticket)
    workflows = generic.GenericRelation(Workflow)

    @property
    def managers(self):
        return self.roles.get(superuser=True).members.all()

    def __unicode__(self):
        return self.name

    def delete(self, using=None):
        self.members.delete()
        return super(Project, self).delete(using)

    def save(self, *args, **kwargs):
        if self.pk is None:
            ret = super(Project, self).save(*args, **kwargs)
            Role.objects.create(project=self, name='Project managers', superuser=True)
            Role.objects.create(project=self, name='Developers')
            self.members = Group.objects.create(name='%s_%d' % (self.name, self.pk))
            return ret

        return super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('project_details', args=[self.pk])

    def on_new_ticket(self, ticket):
        action.send(ticket.submitter, verb='created new ticket', action_object=ticket, target=self)

    def has_perm(self, user, perm):
        pass

class ProjectSearchAdapter(watson.SearchAdapter):
    def get_title(self, obj):
        return obj.name

watson.register(Project, ProjectSearchAdapter)

def modify_project_group(sender, instance, **kwargs):
    if instance.pk:
        a = User.objects.filter(groups=instance.project.members)
        b = User.objects.filter(roles__project=instance.project)
        to_remove = a.exclude(id__in=b)
        to_add = b.exclude(id__in=a)
        for user in to_remove:
            unfollow(user, instance.project)
        for user in to_add:
            follow(user, instance.project, actor_only=False)
        instance.project.members.user_set.add(*to_add)
        instance.project.members.user_set.remove(*to_remove)


pre_save.connect(modify_project_group, sender=Role)

registry.register(Role)
registry.register(Project)
registry.register(Group)
registry.register(User)