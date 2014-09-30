from bootstrap3.forms import render_label
from bootstrap3.renderers import FieldRenderer
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.utils.html import strip_tags


class FieldRenderer(FieldRenderer):
    def put_inside_label(self, html):
        if isinstance(self.widget, RadioSelect):
            icon = 'circle'
        else:
            icon = 'square'

        content = '{field} {label} <i class="fa fa-{icon}-o"></i>'.format(field=html, label=self.field.label, icon=icon)
        return render_label(content=content, label_for=self.field.id_for_label, label_title=strip_tags(self.field_help))

    def post_widget_render(self, html):
        if isinstance(self.widget, CheckboxSelectMultiple):
            html = html.replace('</label>', ' <i class="fa fa-square-o"></i></label>')
        html = super(FieldRenderer, self).post_widget_render(html)
        return html