from django.contrib import admin

# Register your models here.
from user_management.models import Profile
from user_management.models import ProfileAddress
from user_management.models import PasswordResetToken
admin.site.register(Profile)
admin.site.register(ProfileAddress)
admin.site.register(PasswordResetToken)