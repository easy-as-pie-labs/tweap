from django.conf.urls import patterns, url
from user_management import views

urlpatterns = patterns(
    '',
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/(?P<user_id>\d+)/$', views.ViewProfile.as_view(), name='profile'),
    url(r'^profile/$', views.ViewProfile.as_view(), name='profile'),
    url(r'^editprofile/$', views.EditProfile.as_view(), name='profile'),

)
