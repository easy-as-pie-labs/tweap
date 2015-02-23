from django.db import models
from django.forms import ModelForm, Textarea, HiddenInput
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.core.urlresolvers import reverse


class Project(models.Model):
    """
    Model for projects
    """
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=30, default='fa fa-folder-open-o')
    description = models.CharField(max_length=1000, blank=True, null=True)
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

        NotificationEvent = models.get_model('notification_center', 'NotificationEvent')

        # notify all other users in project that the user left
        # see if event type already exists in db
        event_text = "left your project"
        try:
            notification_event = NotificationEvent.objects.get(text=event_text)
        except:
            notification_event = NotificationEvent()
            notification_event.text = event_text
            notification_event.save()

        # send out notifications
        for member in self.members.all():
            a_user = User.objects.get(username=member.username)

            # We don't want a notification for the user who created this
            # also if the post data was manipulated and a user assigned who is not in the project let's ignore it
            if a_user == user or a_user not in self.members.all():
                continue

            notification = Notification()
            notification.receiver = a_user
            notification.trigger_user = user
            notification.project = self
            # target_url is not needed here
            notification.target_url = ''
            notification.event = notification_event
            notification.save()




        # TODO: besprechen ob wir das so wollen
        if self.members.count() == 0:
            if not Invitation.objects.filter(project=self):
                self.delete()
                return

        self.save()

    def has_user(self, user):
        if user in self.members.all():
            return True
        return False


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