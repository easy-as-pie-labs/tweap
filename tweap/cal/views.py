from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext
from django.contrib.auth.models import User
from project_management.models import Project
from project_management.tools import get_tags
from notification_center.models import NotificationEvent, Notification
from cal.models import Event
from cal.tools import validate_for_event
import json

class CreateEdit(View):
    """
    View class for creating or editing an event
    """
    def get(self, request, event_id=None, project_id=None):

        if event_id is None:
            if project_id is None:
                raise Http404

            project = get_object_or_404(Project, id=project_id)

            project_members = project.members.all()

            # redirect if user is not in group at all
            if request.user not in project_members:
                raise Http404

            context = {
                'headline': ugettext("Create new Event"),
                'project': project,
                'members': project.members.all(),
            }

            return render(request, 'cal/create_edit.html', context)

        event = get_object_or_404(Event, id=event_id)

        project = event.project

        # redirect if user is not in group at all
        if request.user not in project.members.all():
            raise Http404
        else:
            context = {
                'headline': ugettext("Edit Event"),
                'event': event,
                'project': project,
            }
        return render(request, 'cal/create_edit.html', context)

    def post(self, request, event_id=None, project_id=None):

        form = request.POST

        if event_id is None:
            if project_id is None:
                raise Http404

            event = Event()
            project = get_object_or_404(Project, id=project_id)
            project_members = project.members.all()

            # redirect if user is not in group at all
            if request.user not in project_members:
                raise Http404

        else:
            event = get_object_or_404(Event, id=event_id)
            project = event.project
            project_members = project.members.all()

            # redirect if user is not in group at all
            if request.user not in project_members:
                raise Http404

        if 'title' in form:
            if form['title'] != "":
                event.title = form['title']
                event.description = form['description']
                event.location = form['location']

                start = form['start']
                if start[-2:] == "PM":
                    start = start[:-3]
                    values = start.split(" ")
                    hour = int(values[1][0:2]) + 12
                    start = str(values[0]) + " " + str(hour) + str(values[1][2:])
                else:
                    start = start[:-3]

                end = form['end']
                if end[-2:] == "PM":
                    end = end[:-3]
                    values = end.split(" ")
                    hour = int(values[1][0:2]) + 12
                    end = str(values[0]) + " " + str(hour) + str(values[1][2:])
                else:
                    end = end[:-3]

                if start == '':
                    context = {
                        'error_messages': {'name': ugettext("Invalid Entry!")},
                        'headline': ugettext("Edit Event"),
                        'project': project,
                    }
                    return render(request, 'cal/create_edit.html', context)

                event.start = start
                event.end = end

                event.project = project
                attendees = form.getlist('attendees')
                event.save()
                event.attendees.clear()
                for attendee in attendees:
                    user = User.objects.get(username=attendee)
                    # if the post data was manipulated and a user assigned who is not in the project let's ignore it
                    if user in project.members.all():
                        event.attendees.add(user)

                event.tags.clear()
                tags = get_tags(form['tags'], event.project)
                for tag in tags:
                    event.tags.add(tag)

                event.save()

                # see if event type already exists in db
                event_text = "assigned an event to you"
                try:
                    notification_event = NotificationEvent.objects.get(text=event_text)
                except:
                    notification_event = NotificationEvent()
                    notification_event.text = event_text
                    notification_event.save()

                # send out notifications
                for attendee in attendees:
                    user = User.objects.get(username=attendee)

                    # We don't want a notification for the user who created this
                    # also if the post data was manipulated and a user assigned who is not in the project let's ignore it
                    if user == request.user or user not in project.members.all():
                        continue

                    notification = Notification()
                    notification.receiver = user
                    notification.trigger_user = request.user
                    notification.project = project
                    notification.target_url = request.build_absolute_uri(reverse('cal:edit', args=(event.id, )))
                    notification.event = notification_event
                    notification.save()

                return HttpResponseRedirect(reverse('project_management:project', args=(project.id, )))

        context = {
            'error_messages': {'name': ugettext("Invalid Entry")},
            'event': event,
            'project': project,
            'headline': ugettext("Create new Event"),
        }
        return render(request, 'cal/create_edit.html', context)

class Delete(View):

    def get(self, request, event_id):

        event = validate_for_event(request, event_id)
        target_url = request.build_absolute_uri(reverse('cal:edit', args=(event.id, )))
        Notification.objects.filter(target_url=target_url).delete()

        event.delete()

        return HttpResponseRedirect(reverse('project_management:project', args=(event.project.id, )))

    def post(self, request, event_id):

        event = validate_for_event(request, event_id)
        target_url = request.build_absolute_uri(reverse('cal:edit', args=(event.id, )))
        Notification.objects.filter(target_url=target_url).delete()
        event.delete()

        return HttpResponseRedirect(reverse('project_management:project', args=(event.project.id, )))


class UpdateFromCalendarView(View):
    """
    handling calendar updates via the interactive cal ui
    :param request:
    :return:
    """
    def post(self, request):
        result = {'url': '', 'id': ''}
        invitation_id = request.POST.get('invitation_id', '')
        action = request.POST.get('action', '')
        if invitation_id:
            invitation = Invitation.objects.get(id=invitation_id)
            if invitation.user == request.user:
                if action == 'accept':
                    invitation.accept()
                    result['url'] = request.build_absolute_uri(reverse('project_management:project', args=(invitation.project.id,)))
                if action == 'reject':
                    invitation.reject()

        return HttpResponse(json.dumps(result), content_type="application/json")

