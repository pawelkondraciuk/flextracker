import os

from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _


class AttachmentManager(models.Manager):
    def attachments_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)


class Attachment(models.Model):
    def attachment_upload(instance, filename):
        """Stores the attachment in a "per module/appname/primary key" folder"""
        if instance.object_id:
            pk = instance.content_object.pk
        else:
            pk = 'temp_%d' % instance.creator.id
        return 'attachments/%s/%s/%s' % (
            '%s_%s' % (instance.content_type.app_label,
                       instance.content_type.name.lower()),
            pk,
            filename)

    objects = AttachmentManager()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(User, related_name="created_attachments", verbose_name=_('creator'))
    attachment_file = models.FileField(_('attachment'), upload_to=attachment_upload)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        ordering = ['-created']
        permissions = (
            ('delete_foreign_attachments', 'Can delete foreign attachments'),
        )

    def __unicode__(self):
        return '%s attached %s' % (self.creator.username, self.attachment_file.name)

    @property
    def filename(self):
        return os.path.split(self.attachment_file.name)[1]

    def is_image(self):
        from PIL import Image

        try:
            Image.open(self.attachment_file.file)
        except IOError:
            return False
        return True