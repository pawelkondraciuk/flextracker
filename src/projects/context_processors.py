from django.db.models.query_utils import Q
from issues.models import Ticket
from projects.models import Project


def project_list(request):
    if request.user.is_authenticated():
        return {'projects': Project.objects.filter(Q(roles__members=request.user, private=True) | Q(private=False)).distinct()}
    return dict()