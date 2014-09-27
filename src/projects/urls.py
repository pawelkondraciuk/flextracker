from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.ProjectListView.as_view(), name='projects'),
    url(r'^create/$', views.CreateProjectView.as_view(), name='create_project'),
    url(r'^(?P<pk>\d+)/$', views.ProjectDetailsView.as_view(), name='project_details'),
    url(r'^(?P<pk>\d+)/edit$', views.EditProjectView.as_view(), name='update_project'),
)