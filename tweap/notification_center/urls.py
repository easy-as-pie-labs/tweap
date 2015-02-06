from django.conf.urls import patterns, url
from notification_center import views

urlpatterns = patterns(
    '',
    url(r'^all/$', views.ViewAll.as_view(), name='view_all'),
    url(r'^view/(?P<notification_id>\d+)/$', views.ViewOne.as_view(), name='view'),
)
