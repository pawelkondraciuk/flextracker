from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^api/', include('workflow.api.urls')),
    url(r'^create/$', views.CreateWorkflow.as_view(), name='create_workflow'),
    url(r'^mapping/(?P<from>\d+)/(?P<to>\d+)$', views.WorkflowMapping.as_view(), name='map_workflow'),
    url(r'^(?P<pk>\d+)/edit/$', views.UpdateWorkflow.as_view(), name='update_workflow'),
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteWorkflow.as_view(), name='delete_workflow'),
)