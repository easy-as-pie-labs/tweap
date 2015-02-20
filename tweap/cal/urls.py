from django.conf.urls import patterns, url
from cal import views

urlpatterns = patterns(
    '',
    url(r'^(?P<event_id>\d+)/?$', views.CreateEdit.as_view(), name='event'),
    url(r'^new/project/(?P<project_id>\d+)$', views.CreateEdit.as_view(), name='create'),
    url(r'^edit/(?P<event_id>\d+)$', views.CreateEdit.as_view(), name='edit'),
    url(r'^delete/(?P<event_id>\d+)$', views.Delete.as_view(), name='delete'),
    url(r'^ui_update/$', views.UpdateFromCalendarView.as_view(), name='ui_update'),
)

