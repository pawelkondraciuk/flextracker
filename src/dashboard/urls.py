from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
)