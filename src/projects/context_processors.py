from projects.models import Project


def project_list(request):
    if request.user.is_authenticated():
        return {'projects': Project.objects.filter(roles__membership__user=request.user)}