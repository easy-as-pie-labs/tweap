from django.conf.urls import patterns, url
from user_management import views

urlpatterns = patterns(
    '',
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^delete/$', views.DeleteAccount.as_view(), name='delete_account'),
    url(r'^profile/(?P<user_name>[A-Za-z0-9]+)/$', views.ViewProfile.as_view(), name='profile'),
    url(r'^editprofile/$', views.EditProfile.as_view(), name='edit_profile'),
    url(r'^upload_picture/$', views.UploadPicture.as_view(), name='upload_picture'),
    url(r'^user_suggestion/$', views.UserSuggestion.as_view(), name='user_suggestion'),
    url(r'^lost_password/$', views.LostPassword.as_view(), name='lost_password'),
    url(r'^reset_password/(?P<reset_token>[a-z0-9]+)/$', views.ResetPassword.as_view(), name='reset_password'),
    url(r'^reset_password/$', views.ResetPassword.as_view(), name='reset_password'),
)
