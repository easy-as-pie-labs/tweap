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


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description')
        widgets = {'description': Textarea()}
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