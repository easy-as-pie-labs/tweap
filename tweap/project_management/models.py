from django.db import models
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from django.utils.translation import ugettext


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def leave(self, user):
        self.members.remove(user)

        #TODO: besprechen ob wir das so wollen
        if self.members.count() == 0:
            if not Invitation.objects.filter(project=self):
                self.delete()
                return

        self.save()


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description')
        widgets = {
            'description': Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'name': ugettext('Name'),
            'description': ugettext('Description')
        }
        error_messages = {
            'name': {
                'max_length': ugettext('The name of the project is too long.')
            }
        }


class Invitation(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

    def accept(self):
        project = Project.objects.get(id=self.project.id)
        user = User.objects.get(id=self.user.id)
        project.members.add(user)
        project.save()
        self.delete()

    def reject(self):
        self.delete()

    @classmethod
    def get_for_user(cls, user):
        return cls.objects.filter(user__id=user.id)

    def __str__(self):
        return self.user.username + " invited to " + self.project.name