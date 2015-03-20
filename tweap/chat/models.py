from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


class Conversation(models.Model):
    members = models.ManyToManyField(User)

    @classmethod
    def get_conversations_of_user(cls, user):
        return Conversation.objects.filter(members=user)

    @classmethod
    def find_by_users_or_create(cls, users):
        conversation = Conversation.objects.annotate(count=Count('members')).filter(members=users[0])
        for user in users[1:]:
            conversation = conversation.filter(members=user)
        conversation.filter(count=len(users))
        if conversation.exists():
            conversation = conversation[0]
        else:
            conversation = Conversation().save()
            for user in users:
                conversation.members.add(user)
            conversation.save()

        return conversation


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    sender = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=2000)

    @classmethod
    def create(cls, conversation, sender, text):
        Message(conversation=conversation, sender=sender, text=text).save()


class AuthToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=32)

    @classmethod
    def get_for_user(cls, user):
        return AuthToken.objects.filter(user=user)

    @classmethod
    def create_or_update_for_user(cls, user, new_token, old_token=None):
        if not old_token:
            AuthToken(user=user, token=new_token).save()
        else:
            token = AuthToken.objects.filter(user=user, token=old_token)
            token.token = new_token
            token.save()