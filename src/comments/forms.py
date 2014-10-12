from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from attachments.models import Attachment
from comments.models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)

    def save(self, request, obj, *args, **kwargs):
        self.instance.author = request.user
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_id = obj.id
        super(CommentForm, self).save(*args, **kwargs)