from project_management.models import Invitation, Tag
from django.contrib.auth.models import User
import re, json


def invite_users(users, project):
    """
    invites one or more user to a project
    :param users: a list of user names and/or email addresses as JSON string
    :param project: the project to which the users should be invited
    :return:
    """
    if users:
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


def get_tags(tag_list, project):
    """
    gets tags from db or create if not exists
    :param tag_list: a list of tags as JSON string
    :param project: the project the tags should be added to
    :return: list of tag objects
    """
    tags = []
    if tag_list:
        tag_list = json.loads(tag_list)
        for tag in tag_list:
            tag = tag.lower().strip()
            if tag:
                try:
                    tag_object = Tag.objects.get(project=project, name=tag)
                except Tag.DoesNotExist:
                    tag_object = Tag(project=project, name=tag)
                    try:
                        tag_object.save()
                    # if someone manipulates post-data and tries to create tags longer than 20 chars
                    except:
                        tag_object = None
                if tag_object is not None:
                    tags.append(tag_object)

    # TODO: check if tags are in project that are used nowhere and delete them!
    return tags


