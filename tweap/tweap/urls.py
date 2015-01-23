from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^users/', include('user_management.urls', namespace='user_management')),
    url(r'^projects/', include('project_management.urls', namespace='project_management')),
    url(r'^admin/', include(admin.site.urls)),
)
