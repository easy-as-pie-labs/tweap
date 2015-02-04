from django.conf.urls import patterns, url
from todo import views

urlpatterns = patterns(
    '',
    url(r'^new/project/(?P<project_id>\d+)$', views.CreateEdit.as_view(), name='create'),
    url(r'^edit/(?P<todo_id>\d+)/$', views.CreateEdit.as_view(), name='edit'),
)
