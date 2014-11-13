from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
)