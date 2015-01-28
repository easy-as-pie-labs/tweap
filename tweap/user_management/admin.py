from django.contrib import admin

# Register your models here.
from user_management.models import Profile
from user_management.models import ProfileAddress
admin.site.register(Profile)
admin.site.register(ProfileAddress)