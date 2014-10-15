from django.conf.urls import patterns, url

from attachments.views import AddAttachmentView


urlpatterns = patterns('',
                       url(r'^add-for/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<pk>\d+)/$',
                           AddAttachmentView.as_view(), name="add_attachment"),
                       url(r'^add-for/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/$', AddAttachmentView.as_view(),
                           name="add_temp_attachment", ),
                       url(r'^delete/(?P<attachment_pk>\d+)/$', 'attachments.views.delete_attachment',
                           name="delete_attachment"),
)