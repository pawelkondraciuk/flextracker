from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteComment.as_view(), name='comment-delete'),
)