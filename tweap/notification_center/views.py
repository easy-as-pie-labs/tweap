from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext
from todo.models import Todo
from django.contrib.auth.models import User
from project_management.models import Project
from notification_center.models import Notification
from project_management.tools import get_tags


class ViewAll(View):
    def get(self, request):
        notifications = Notification.objects.filter(receiver=request.user)

        return render(request, 'notification_center/view_all.html', {'notifications': notifications})


class ViewOne(View):
    def get(self, request, notification_id):
        notification = Notification.objects.get(id=notification_id)
        url = notification.url.url
        parameter = notification.url.parameter
        notification.delete()
        return HttpResponseRedirect(reverse(url, args=(parameter, )))
