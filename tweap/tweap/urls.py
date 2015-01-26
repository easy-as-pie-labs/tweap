from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^users/', include('user_management.urls', namespace='user_management')),
    url(r'^projects/', include('project_management.urls', namespace='project_management')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'^rosetta/', include('rosetta.urls')),
    )
