from django.conf.urls import patterns, url
from chat import views

urlpatterns = patterns(
    '',
    url(r'^get-messages/$', views.Messages.as_view(), name='view_all'),
    url(r'^node-api/$', views.NodeAPI.as_view(), name='node_api'),
)
