from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


class Conversation(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    members = models.ManyToManyField(User)

    @classmethod
    def get_conversations_of_user(cls, user):
        return Conversation.objects.filter(members=user)

    @classmethod
    def find_by_users_or_create(cls, users):
        conversation = Conversation.objects.filter(members=users[0]).annotate(count=Count('members'))
        for user in users[1:]:
            conversation = conversation.filter(members=user)
        conversation.filter(count=len(users))
        if conversation.exists():
            conversation = conversation[0]
        else:
            conversation = Conversation()
            conversation.save()
            conversation.members.add(*users)
            conversation.save()

        return conversation

    def get_messages(self, side, message=None):
        count = Message.objects.filter(conversation=self).count()
        if count == 0:
            return []
        if message and side == 'oldest':
            messages = Message.objects.filter(conversation=self).filter(timestamp__lt=message.timestamp)[:20]
        elif message and side == 'newest':
            messages = Message.objects.filter(conversation=self).filter(timestamp__gt=message.timestamp).order_by('timestamp')[:20]
        else:
            messages = Message.objects.filter(conversation=self)[:20]

        result_messages = messages.values('text')
        for i in range(0, len(result_messages)):
            date = str("%04d" % messages[i].timestamp.year) + "-" + str("%02d" % messages[i].timestamp.month) + "-" + str("%02d" % messages[i].timestamp.day)
            time = str("%02d" % messages[i].timestamp.hour) + ":" + str("%02d" % messages[i].timestamp.minute + ":"+ str("%02d" % messages[i].timestamp.second))
            result_messages[i]['timestamp'] = date + " " + time
            result_messages[i]['sender'] = messages[i].sender.username
            result_messages[i]['conversation'] = messages[i].conversation.id

        return list(result_messages)

    def __str__(self):
        return "Conversation " + str(self.id)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    sender = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=2000)

    class Meta:
        ordering = ['-timestamp']

    @classmethod
    def create(cls, conversation, sender, text):
        Message(conversation=conversation, sender=sender, text=text).save()

    def __str__(self):
        return "Message in Conversation " + str(self.conversation.id) +  " from " + self.sender.username + " at " + str(self.timestamp)


class AuthToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=32)

    @classmethod
    def create_or_update_for_user(cls, user, new_token, old_token=None):
        if not old_token:
            AuthToken(user=user, token=new_token).save()
        else:
            token = AuthToken.objects.get(user=user, token=old_token)
            token.token = new_token
            token.save()

    def __str__(self):
        return "AuthToken of " + self.user.username