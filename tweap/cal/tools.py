from django.shortcuts import get_object_or_404
from cal.models import Event
from django.http import Http404, HttpResponse
import base64
from django.contrib.auth import authenticate


def validate_for_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    project = event.project

    if project.has_user(request.user):
        return event
    raise Http404


def basic_auth_checker(view, request, realm="", *args, **kwargs):
    """
    checks the basic auth
    """
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).decode("ascii").split(':')
                uname.strip().lower()
                passwd.strip()
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    request.user = user
                    return view(request, *args, **kwargs)

    # authentication failed
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return response


def basicauth(realm=""):
    """
    returns a decorator for base_auth
    """
    def view_decorator(func):
        def wrapper(request, *args, **kwargs):
            return basic_auth_checker(func, request, realm, *args, **kwargs)
        return wrapper
    return view_decorator