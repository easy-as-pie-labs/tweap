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
from cal.tools import validate_for_event, basicauth
import json
from datetime import datetime
import pytz
from icalendar import Calendar as iCal, Event as iEvent

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
                'headline': ugettext("Create new Event in") + " " + project.name,
                'project': project,
                'members': project.members.order_by('username'),
                'invitees': project.get_invited_users(),
                'start': request.GET.get('start', ''),
                'end': request.GET.get('end', ''),
            }

            return render(request, 'cal/create_edit.html', context)

        event = get_object_or_404(Event, id=event_id)

        project = event.project

        # redirect if user is not in group at all
        if request.user not in project.members.all():
            raise Http404
        else:
            context = {
                'headline': ugettext("Edit Event in") + " " + project.name,
                'event': event,
                'project': project,
                'members': project.members.order_by('username'),
                'invitees': project.get_invited_users(),
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
                end = form['end']

                if start == '' or end == '':
                    context = {
                        'error_messages': {'name': ugettext("Invalid Entry!")},
                        'headline': ugettext("Edit Even in") + " " + project.name,
                        'project': project,
                    }
                    return render(request, 'cal/create_edit.html', context)

                event.start = pytz.utc.localize(datetime.strptime(start, "%Y-%m-%d %H:%M"))
                event.end = pytz.utc.localize(datetime.strptime(end, "%Y-%m-%d %H:%M"))

                if event.start > event.end:
                    context = {
                        'error_messages': {'name': ugettext("Invalid Entry!")},
                        'headline': ugettext("Edit Event in ") + " " + project.name,
                        'project': project,
                    }
                    return render(request, 'cal/create_edit.html', context)

                event.project = project
                attendees = form.getlist('attendees')
                event.save()

                #Get already assigned attendees, for notification sending
                already_assigned_attendees = []

                for attendee in attendees:
                    user = User.objects.get(username=attendee)
                    if user in event.attendees.all():
                        already_assigned_attendees.append(user)

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

                # create notifications for all attendees
                Notification.bulk_create(attendees, request.user, project, request.build_absolute_uri(reverse('cal:edit', args=(event.id, ))), 'added you to an event')

                return HttpResponseRedirect(reverse('project_management:project', args=(project.id, )))

        context = {}
        context['error_messages'] = {'name': ugettext("Invalid Entry")}
        context['project'] = project
        if event_id is not None:
            context['event'] = event
            context['headline'] = ugettext("Edit Event in ") + " " + project.name
        else:
            context['headline'] = ugettext("Create new Event in") + " " + project.name
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
        result = {'success': 'true'}
        event_id = request.POST.get('event_id', '')
        start_time = request.POST.get('start', '')
        end_time = request.POST.get('end', '')

        try:
            event = Event.objects.get(id=event_id)
            event.start = pytz.utc.localize(datetime.strptime(start_time, "%Y-%m-%d %H:%M"))
            print(event.start)
            event.end = pytz.utc.localize(datetime.strptime(end_time, "%Y-%m-%d %H:%M"))
            event.save()

        except:
            result = {'success': 'false'}

        return HttpResponse(json.dumps(result), content_type="application/json")


@basicauth()
def userfeed(request):
    cal = iCal()

    # get all events for user
    events = Event.get_all_events_for_userprojects(request.user)

    # add all events to calendar
    for event in events:
        url = request.build_absolute_uri(reverse('cal:edit', args=(event.id, )))
        cal.add_component(make_i_event(event, url))

    stream = cal.to_ical()#.replace('\r\n', '\n').strip()

    response = HttpResponse(stream, content_type='text/calendar; charset=utf-8')
    response['Filename'] = request.user.username + '.ics'
    response['Content-Disposition'] = 'attachment; filename=' + request.user.username + '.ics'

    return response

@basicauth()
def projectfeed(request, project_id):
    cal = iCal()

    project = get_object_or_404(Project, id=project_id, members=request.user)
    events = Event.get_all_project_events_for_user(project)

    # add all events to calendar
    for event in events:
        url = request.build_absolute_uri(reverse('cal:edit', args=(event.id, )))
        cal.add_component(make_i_event(event, url))

    stream = cal.to_ical()#.replace('\r\n', '\n').strip()

    response = HttpResponse(stream, content_type='text/calendar; charset=utf-8')
    response['Filename'] = project.name + '.ics'
    response['Content-Disposition'] = 'attachment; filename=' + project.name + '.ics'

    return response


def make_i_event(event, url):
    """
    creates iEvent from cal event
    :param event: cal event
    :param url: url of said event
    :return:
    """
    e = iEvent()
    e.add('summary', event.title)

    description = event.description
    if len(event.attendees.all()) > 0:
        description += " - attended by"
    for user in event.attendees.all():
        description += " " + user.username + ","
    description = description[:-1]

    e.add('url', url)
    e.add('description', description)
    e.add('location', event.location)
    e.add('dtstart', event.start.replace(tzinfo=pytz.timezone("Europe/Berlin")))
    e.add('dtend', event.end.replace(tzinfo=pytz.timezone("Europe/Berlin")))
    return e