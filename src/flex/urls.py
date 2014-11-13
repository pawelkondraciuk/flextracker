from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
   # Examples:
   # url(r'^$', 'flex.views.home', name='home'),
   # url(r'^blog/', include('blog.urls')),
   url(r'^hook/', include('github_hook.urls')),
   url(r'^grappelli/', include('grappelli.urls')),
   url(r'^inbox/messages/', include('django_messages.urls')),
   url(r'^attachments/', include('attachments.urls')),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^accounts/', include('userena.urls')),
   url(r'^workflow/', include('workflow.urls')),
   url(r'^projects/', include('projects.urls')),
   url(r'^projects/', include('issues.urls')),
   url(r'^comments/', include('comments.urls')),
   url(r'^', include('dashboard.urls')),
   url(r'^', include('accounts.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
