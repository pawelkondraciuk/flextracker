from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
   # Examples:
   # url(r'^$', 'flex.views.home', name='home'),
   # url(r'^blog/', include('blog.urls')),

   url(r'^admin/', include(admin.site.urls)),
   url(r'^accounts/', include('userena.urls')),
   url(r'^projects/', include('projects.urls')),
   url(r'^projects/', include('issues.urls')),
   url(r'^', include('dashboard.urls')),
)
