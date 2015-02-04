from django.conf.urls import patterns, url
from todo import views
from project_management import views as projectviews

urlpatterns = patterns(
    '',
    url(r'^(?P<todo_id>\d+)/?$', views.CreateEdit.as_view(), name='todo'),
    url(r'^new/project/(?P<project_id>\d+)$', views.CreateEdit.as_view(), name='create'),
    url(r'^edit/(?P<todo_id>\d+)/$', views.CreateEdit.as_view(), name='edit'),
    url(r'^delete/(?P<todo_id>\d+)/$', views.Delete.as_view(), name='delete'),
    url(r'^clear/(?P<todo_id>\d+)/$', views.CreateEdit.as_view(), name='clear'),
)
