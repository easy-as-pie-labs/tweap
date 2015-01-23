from project_management.models import Invitation
from django.contrib.auth.models import User
import re


def invite_users(users, project):
    users = users.split(',')
    for user in users:
        user = user.lower().strip()
        try:
            if re.match("[^@]+@[^@]+\.[^@]+", user):
                user_object = User.objects.get(email=user)
            else:
                user_object = User.objects.get(username=user)

            Invitation(user=user_object, project=project).save()

        except User.DoesNotExist:
            pass
            # TODO: send invitation to non tweap-user via email