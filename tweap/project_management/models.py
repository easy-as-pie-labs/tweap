from django.db import models
from django.forms import ModelForm, Textarea, HiddenInput
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.core.urlresolvers import reverse
from chat.models import Conversation


class Project(models.Model):
    """
    Model for projects
    """
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=30, default='fa fa-folder-open-o')
    description = models.CharField(max_length=1000, blank=True, null=True)
    conversation = models.ForeignKey(Conversation, null=True, blank=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def leave(self, user):
        """
        removes the given user from the project
        deletes the project if no user remains in the project
        :param user: the user who should be removed
        :return:
        """
        self.members.remove(user)
        self.save()

        if self.conversation is not None:
            self.conversation.members.remove(user)
            self.conversation.save()


        # because circular imports are not allowed
        # models.get_model needs to be used here

        # remove user from all todoh assignments in this project
        Todo = models.get_model('todo', 'Todo')
        todos = Todo.objects.filter(assignees=user, project=self)
        for todo in todos:
            todo.remove_assignee(user)

        # remove user from all cal attendees in this project
        Event = models.get_model('cal', 'Event')
        events = Event.objects.filter(attendees=user, project=self)
        for event in events:
            event.remove_attendee(user)

        # remove all Notifications concerning this project
        Notification = models.get_model('notification_center', 'Notification')
        Notification.objects.filter(receiver=user, project=self).delete()

        # notify all project users
        target_url = reverse('project_management:project', args=(self.id, ))
        Notification.project_notification(user, self, target_url, 'left the project')

        if self.members.count() == 0:
            if not Invitation.objects.filter(project=self):
                if self.conversation is not None:
                    self.conversation.delete()
                self.delete()
                return

    def has_user(self, user):
        if user in self.members.all():
            return True
        return False

    def get_invited_users(self):
        invitations = Invitation.objects.filter(project=self)
        users = []
        for invite in invitations:
            users.append(invite.user)
        return users


class ProjectForm(ModelForm):
    """
    Form for the project model
    """
    class Meta:
        model = Project
        fields = ('icon', 'name', 'description')
        widgets = {
            'description': Textarea(attrs={'class': 'form-control'}),
            'icon': HiddenInput()
        }
        labels = {
            'name': ugettext_lazy('Name'),
            'description': ugettext_lazy('Description')
        }
        error_messages = {
            'name': {
                'max_length': ugettext_lazy('The name of the project is too long.')
            }
        }


class Invitation(models.Model):
    """
    Model for invitations
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

    def accept(self):
        """
        accepts the invitation, adds the user to the project and deletes the invitation
        :return:
        """
        project = Project.objects.get(id=self.project.id)
        user = User.objects.get(id=self.user.id)
        project.members.add(user)
        project.save()

        if project.conversation is not None:
            project.conversation.members.add(user)
            project.conversation.save()

        self.delete()

    def reject(self):
        """
        deletes the invitation
        :return:
        """
        self.delete()

    @classmethod
    def get_for_user(cls, user):
        """
        creates a list of all invitations of a given user
        :param user: the user for which invitations are looked for
        :return: the list of invitations
        """
        return cls.objects.filter(user__id=user.id)

    def __str__(self):
        return self.user.username + " invited to " + self.project.name


class Tag(models.Model):
    """
    Model for Todo tags
    """
    name = models.CharField(max_length=20)
    project = models.ForeignKey(Project)

    def __str__(self):
        return self.name + " in " + self.project.name