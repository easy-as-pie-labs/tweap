from django.conf.urls import patterns, url
from project_management import views

urlpatterns = patterns(
    '',
    url(r'^(?P<project_id>\d+)/?$', views.Project.as_view(), name='project'),
    url(r'^new/$', views.Create.as_view(), name='create'),
    url(r'^edit/(?P<project_id>\d+)/$', views.Edit.as_view(), name='edit'),
    url(r'^all/$', views.ViewAll.as_view(), name='view_all'),
    url(r'^invites/$', views.view_invites, name='view_invites'),
    url(r'^leave_group/(?P<project_id>\d+)/?$', views.leave_group, name='leave_group'),
    url(r'^accept_invite/(?P<project_id>\d+)/?$', views.accept_invite, name='accept_invite'),
    url(r'^reject_invite/(?P<project_id>\d+)/?$', views.reject_invite, name='reject_invite'),

)
