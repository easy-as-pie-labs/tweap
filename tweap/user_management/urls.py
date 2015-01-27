from django.conf.urls import patterns, url
from user_management import views

urlpatterns = patterns(
    '',
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/((?P<user_name>[A-Za-z0-9]+)/)?$', views.ViewProfile.as_view(), name='profile'),
    url(r'^editprofile/$', views.EditProfile.as_view(), name='edit_profile'),
    url(r'^upload_picture/$', views.upload_picture, name='upload_picture'),
    url(r'^user_suggestion/$', views.user_suggestion, name='user_suggestion'),

)
