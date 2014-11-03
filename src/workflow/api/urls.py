from django.conf.urls import include, patterns, url
from . import api

urlpatterns = patterns('',
    url(r'^project/(?P<project_id>\d+)/$', api.WorkflowListAPIView.as_view(), name='workflow-list-api'),
    url(r'^(?P<pk>\d+)/$', api.WorkflowAPIView.as_view(), name='workflow-api'),
    url(r'^create/$', api.CreateWorkflowAPIView.as_view(), name='create-workflow-api'),
    url(r'^status/$', api.CreateStatusAPIView.as_view(), name='create-status-api'),
    url(r'^status/(?P<pk>\d+)/$', api.UpdateStatusAPIView.as_view(), name='update-status-api'),
)
