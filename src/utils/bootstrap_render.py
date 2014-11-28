from bootstrap3.forms import render_label
from bootstrap3.renderers import FieldRenderer
from django.core.urlresolvers import reverse
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.utils.html import strip_tags
from projects.forms import WorkflowRadioSelect


class CustomFieldRenderer(FieldRenderer):
    def put_inside_label(self, html):
        if isinstance(self.widget, RadioSelect):
            icon = 'circle'
        else:
            icon = 'square'

        content = u'{field} {label} <i class="fa fa-{icon}-o"></i>'.format(field=html, label=self.field.label, icon=icon)
        return render_label(content=content, label_for=self.field.id_for_label, label_title=strip_tags(self.field_help))

    def post_widget_render(self, html):
        if isinstance(self.widget, CheckboxSelectMultiple):
            html = html.replace('</label>', ' <i class="fa fa-square-o"></i></label>')
        elif isinstance(self.widget, WorkflowRadioSelect):
            for choice in self.widget.choices.queryset:
                html = html.replace(choice.name, '%s <i class="fa fa-circle-o"></i></label>' % choice.name)
        elif isinstance(self.widget, RadioSelect):
            html = html.replace('</label>', ' <i class="fa fa-circle-o"></i></label>')
        html = super(CustomFieldRenderer, self).post_widget_render(html)
        return html