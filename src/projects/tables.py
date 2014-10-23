# tutorial/tables.py
import django_tables2 as tables
from django_tables2.utils import A

from projects.models import Project


class CustomTextLinkColumn(tables.LinkColumn):
    def __init__(self, viewname, urlconf=None, args=None,
                 kwargs=None, current_app=None, attrs=None, custom_text=None, **extra):
        super(CustomTextLinkColumn, self).__init__(viewname, urlconf=urlconf,
                                                   args=args, kwargs=kwargs, current_app=current_app, attrs=attrs,
                                                   **extra)
        self.custom_text = custom_text


    def render(self, value, record, bound_column):
        return super(CustomTextLinkColumn, self).render(
            self.custom_text if self.custom_text else value,
            record, bound_column)


class ProjectTable(tables.Table):
    code = tables.LinkColumn('project_details', kwargs={'pk': A('pk')})

    class Meta:
        model = Project
        order_by = ('-created',)
        fields = ('code', 'name', 'created')