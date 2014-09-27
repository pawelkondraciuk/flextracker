from braces.views._access import LoginRequiredMixin
from django.views.generic.base import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'

