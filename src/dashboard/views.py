from abc import abstractmethod
import re
import urllib
from braces.views._access import LoginRequiredMixin
from dateutil.parser import parse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.constants import ERROR
from django.contrib.redirects.models import Redirect
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
import watson
from watson.views import SearchMixin
from comments.models import Comment
from github_hook.models import hook_signal
from issues.models import Ticket
from projects.models import Project
from django.utils.translation import ugettext_lazy as _


class MatchException(Exception):
    pass

class RegexResolver(object):
    regex = None
    def resolve(self, query):
        for match in re.finditer(self.regex, query):
            yield match

class AssignedResolver(RegexResolver):
    regex = '(?:assigned to @([\w_-]+))'

    def resolve(self, query):
        q = {}
        match = re.match(self.regex, query)

        if match and match.group(1):
            if User.objects.filter(username=match.group(1)).exists():
                q = {'assigned_to': match.group(1)}
            else:
                raise MatchException(_('User not found'))

        return q

class SubmittedResolver(RegexResolver):
    regex = '(?:submitted)(?:(?: by @([\w_-]+)(?:(?:.*?) on ([\w_-]+))?)|(?: on ([\w_-]+)))'

    def resolve(self, query):
        q = {}
        match = re.search(self.regex, query)

        if match and match.group(1):
            if User.objects.filter(username=match.group(1)).exists():
                q.update({'submitter': match.group(1)})
            else:
                raise MatchException(_('User not found'))

        if match and (match.group(2) or match.group(3)):
            try:
                q.update({'created': parse(match.group(2) or match.group(3)).date()})
            except:
                pass

        return q

class Resolver(object):
    @classmethod
    def user(self, query):
        match = re.search('^@([\w_-]+)$', query)
        if match:
            if User.objects.filter(username=match.group(1)).exists():
                return match.group(1)
            else:
                raise MatchException(_('User not found'))
        else:
            return None

    @classmethod
    def ticket(self, query):
        match = re.match('^\[([\w_-]+)\]$', query)
        if match:
            if Ticket.objects.filter(slug=match.group(1)).exists():
                return match.group(1)
            else:
                raise MatchException(_('Ticket not found'))
        else:
            return None

class ActionResolver(object):
    def __init__(self, user):
        self.user = user

    def resolve(self, query, commit_id=None):
        self.query = query
        self.commit_id = commit_id
        return self.assign_action() or self.action()

    def assign_action(self):
        assign_action = '^(?:assign (?:\[([\w_-]+)\]) (?:to) @([\w_-]+))$'

        query = self.query

        assign_match = re.match(assign_action, query)
        if assign_match:
            ticket = assign_match.group(1)
            username = assign_match.group(2)

            if not Ticket.objects.filter(slug=ticket).exists():
                raise MatchException(_('Ticket not found'))

            if not User.objects.filter(username=username).exists():
                raise MatchException(_('User not found'))

            ticket = Ticket.objects.get(slug=ticket)
            user = User.objects.get(username=username)

            ticket.assigned_to = user
            ticket._user = user
            ticket.save()

            if self.commit_id:
                issue_type = ContentType.objects.get_for_model(self.object)
                Comment.objects.create(content='Assigned ticket to %s #%s' % (user.username, self.commit_id), author=self.user, content_type=issue_type, object_id=ticket.id)

            return redirect(ticket.get_absolute_url())

        return None

    def action(self):
        regex = '(\w+) (?:\[([\w_-]+)\])'
        action_match = re.match(regex, self.query)

        if action_match:
            action = action_match.group(1)
            ticket = action_match.group(2)

            if not Ticket.objects.filter(slug=ticket).exists():
                raise MatchException(_('Ticket not found'))

            ticket = Ticket.objects.get(slug=ticket)
            project = Project.objects.get(pk=ticket.object_id)

            if action.lower() == 'close':
                if ticket.status == project.workflow.end_state:
                    return redirect(ticket.get_absolute_url())
                ticket.status = project.workflow.end_state
                ticket._user = self.user
                ticket.save()

                if self.commit_id:
                    issue_type = ContentType.objects.get_for_model(Ticket)
                    Comment.objects.create(content='Closed ticket #%s' % self.commit_id, author=self.user, content_type=issue_type, object_id=ticket.id)
            else:
                raise MatchException(_('Unrecognized action'))

            return redirect(ticket.get_absolute_url())

        return None


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

class SearchView(SearchMixin, ListView):
    template = 'watson/search_results.html'

    def get(self, request, *args, **kwargs):

        query = self.get_query(request)
        try:
            user = Resolver.user(query)
            if user:
                return redirect(reverse('userena_profile_detail', args=[user]))

            ticket = Resolver.ticket(query)
            if ticket:
                return redirect(Ticket.objects.get(slug=ticket).get_absolute_url())

            if self.request.user.is_authenticated():
                resolver = ActionResolver(request.user).resolve(query)
                if resolver:
                    return resolver

            q = {}
            q.update(AssignedResolver().resolve(query))
            q.update(SubmittedResolver().resolve(query))

            if q:
                q.update({'q': query})
                return redirect(reverse('all_issues') + '?' + urllib.urlencode(q))
        except MatchException as e:
            messages.add_message(request, ERROR, str(e))
            return render(request, 'error.html')

        return super(SearchView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return watson.search(self.query, models=self.get_models(), exclude=self.get_exclude())

def processWebhook(sender, **kwargs):
    if not Project.objects.filter(github_hook=kwargs['payload']['repository']['html_url']).exists():
        return

    for commit in kwargs['payload']['commits']:
        try:
            author = User.objects.get(email=commit['author']['email'])
        except User.DoesNotExist:
            return

        ActionResolver(author).resolve(commit['message'], commit['id'])


hook_signal.connect(processWebhook)