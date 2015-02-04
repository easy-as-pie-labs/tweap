from django.conf.urls import patterns, url
from project_management import views

urlpatterns = patterns(
    '',
    url(r'^(?P<todo_id>\d+)/?$', views.Todo.as_view(), name='todo'),
    url(r'^new/forproject/(?P<project_id>\d+)$', views.CreateEdit.as_view(), name='create'),
    url(r'^edit/(?P<todo_id>\d+)/$', views.CreateEdit.as_view(), name='edit'),
)
