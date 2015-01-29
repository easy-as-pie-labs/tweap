from django.conf.urls import patterns, url
from project_management import views

urlpatterns = patterns(
    '',
    url(r'^(?P<project_id>\d+)/?$', views.Project.as_view(), name='project'),
    url(r'^new/$', views.CreateEdit.as_view(), name='create'),
    url(r'^edit/(?P<project_id>\d+)/$', views.CreateEdit.as_view(), name='edit'),
    url(r'^leave/$', views.leave, name='leave'),
    url(r'^all/$', views.ViewAll.as_view(), name='view_all'),
    url(r'^invites/$', views.view_invites, name='view_invites'),
    url(r'^invitation_handler/$', views.invitation_handler, name='invitation_handler'),
)
