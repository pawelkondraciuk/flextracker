from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    #url(r'^$', views.ProjectListView.as_view(), name='projects'),
    #url(r'^(?P<pk>\d+)/create/$', views.CreateIssueView.as_view(), name='create_issue'),
)