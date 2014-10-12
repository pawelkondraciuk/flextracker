import json
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views import generic
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from attachments.models import Attachment
from attachments.forms import AttachmentForm

def add_url_for_obj(obj):
    return reverse('add_attachment', kwargs={
                        'app_label': obj._meta.app_label,
                        'module_name': obj._meta.module_name,
                        'pk': obj.pk
                    })

@require_POST
@login_required
def add_attachment(request, app_label, module_name, pk,
                   template_name='attachments/add.html', extra_context={}):

    model = get_model(app_label, module_name)
    if model is None:
        return HttpResponseRedirect(next)
    obj = get_object_or_404(model, pk=pk)
    form = AttachmentForm(request.POST, request.FILES)

    if form.is_valid():
        form.save(request, obj)
        return HttpResponse()
    else:
        template_context = {
            'form': form,
            'form_url': add_url_for_obj(obj),
            'next': next,
        }
        template_context.update(extra_context)
        return render_to_response(template_name, template_context,
                                  RequestContext(request))

class AddAttachmentView(generic.FormView):
    form_class = AttachmentForm
    template_name = 'attachments/add.html'

    def form_valid(self, form):
        model = get_model(self.kwargs.get('app_label'), self.kwargs.get('module_name'))
        if model is None:
            return HttpResponseRedirect(next)
        obj = get_object_or_404(model, pk=self.kwargs.get('pk'))

        form.save(self.request, obj)

        return HttpResponse(json.dumps(), status=200)

    def form_invalid(self, form):
        return HttpResponse(status=400)

    def get_context_data(self, **kwargs):
        context = super(AddAttachmentView, self).get_context_data(**kwargs)

        model = get_model(self.kwargs.get('app_label'), self.kwargs.get('module_name'))
        if model is None:
            return HttpResponseRedirect(next)
        obj = get_object_or_404(model, pk=self.kwargs.get('pk'))

        context.update({
            'form_url': add_url_for_obj(obj),
            'next': next,
        })
        return context

@login_required
def delete_attachment(request, attachment_pk):
    g = get_object_or_404(Attachment, pk=attachment_pk)
    if request.user.has_perm('delete_foreign_attachments') \
       or request.user == g.creator:
        g.delete()
        request.user.message_set.create(message=ugettext('Your attachment was deleted.'))
    next = request.REQUEST.get('next') or '/'
    return HttpResponseRedirect(next)
