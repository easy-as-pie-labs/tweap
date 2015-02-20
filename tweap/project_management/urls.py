from django.conf.urls import patterns, url
from project_management import views

urlpatterns = patterns(
    '',
    url(r'^(?P<project_id>\d+)/?$', views.ProjectView.as_view(), name='project'),
    url(r'^new/$', views.CreateEdit.as_view(), name='create'),
    url(r'^edit/(?P<project_id>\d+)/$', views.CreateEdit.as_view(), name='edit'),
    url(r'^leave/$', views.LeaveGroup.as_view(), name='leave'),
    url(r'^invitation_handler/$', views.InvitationHandler.as_view(), name='invitation_handler'),
    url(r'^tag_suggestion/$', views.TagSuggestion.as_view(), name='tag_suggestion'),
)
