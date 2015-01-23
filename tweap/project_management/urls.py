from django.conf.urls import patterns, url
from project_management import views

urlpatterns = patterns(
    '',
    url(r'^(?P<project_id>\d+/)?$', views.Project.as_view(), name='project'),
    url(r'^new/$', views.Create.as_view(), name='create'),

)
