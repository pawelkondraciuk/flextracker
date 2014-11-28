# tutorial/tables.py
from django.utils.html import escape
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2.utils import A
from accounts.models import UserProfile
from django.utils.translation import ugettext_lazy as _


class ImageColumn(tables.Column):
    def render(self, value):
        return mark_safe('<img src="%s" class="img-rounded avatar"/>'
                         % escape(value))


class UserTable(tables.Table):
    user_avatar = ImageColumn('Avatar', accessor='get_mugshot_url', orderable=False, )
    username = tables.LinkColumn(verbose_name=_('Username'), 'userena_profile_detail', accessor='user.username', args=[A('user.username')])

    class Meta:
        model = UserProfile
        fields = ('user_avatar', 'username', 'user.first_name', 'user.last_name')