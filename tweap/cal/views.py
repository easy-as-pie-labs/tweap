from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext
from django.contrib.auth.models import User
from project_management.models import Project
from project_management.tools import get_tags
from notification_center.models import NotificationEvent, Notification
import json

class CreateEdit(View):
    """
    View class for creating or editing an event
    """
    def get(self, request, event_id=None, project_id=None):

        """if event_id is None:
            if project_id is None:
                raise Http404

            project = get_object_or_404(Project, id=project_id)

            project_members = project.members.all()

            #redirect if user is not in group at all
            if request.user not in project_members:
                raise Http404

            context"""

    def post(self, request, event_id=None, project_id=None):
        return "empty"

class Delete(View):

    def get(self, request, event_id):
        return "empty"

    def post(self, request, event_id):
        return "empty"


