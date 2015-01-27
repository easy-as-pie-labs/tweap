from project_management.models import Invitation
from django.contrib.auth.models import User
import re, json


def invite_users(users, project):
    users = json.loads(users)
    for user in users:
        user = user.lower().strip()
        try:
            if re.match("[^@]+@[^@]+\.[^@]+", user):
                user_object = User.objects.get(email=user)
            else:
                user_object = User.objects.get(username=user)

            if not Invitation.objects.filter(user__id=user_object.id, project__id=project.id).exists() and user_object not in project.members.all():
                Invitation(user=user_object, project=project).save()

        except User.DoesNotExist:
            pass
            # TODO: send invitation to non tweap-user via email