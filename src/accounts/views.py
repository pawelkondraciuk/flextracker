from django.views.generic.edit import FormView, UpdateView
from accounts.models import UserProfile


class SettingsView(UpdateView):
    template_name = 'accounts/settings.html'
    model = UserProfile
    fields = ('email_notifications',)
    success_url = '.'

    def get_object(self, queryset=None):
        return self.request.user.profile