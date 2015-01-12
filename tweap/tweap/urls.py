from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^user_management/', include('user_management.urls', namespace='user_management')),
    url(r'^admin/', include(admin.site.urls)),
)
