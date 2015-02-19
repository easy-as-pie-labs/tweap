from django.shortcuts import get_object_or_404
from cal.models import Event
from django.http import Http404

def validate_for_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    project = event.project

    if request.user not in project.members.all():
        raise Http404
    return event
