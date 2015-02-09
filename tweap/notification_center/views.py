from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from notification_center.models import Notification


class ViewAll(View):
    def get(self, request):
        notifications = Notification.objects.filter(receiver=request.user)

        return render(request, 'notification_center/view_all.html', {'notifications': notifications})


class ViewOne(View):
    def get(self, request, notification_id):
        # TODO: error handling
        notification = Notification.objects.get(id=notification_id)
        url = notification.target_url
        notification.delete()
        return HttpResponseRedirect(url)


class MarkSeen(View):
    def get(self, request, notification_id):
        notification = Notification.objects.get(id=notification_id)
        url = notification.target_url
        notification.delete()
        return HttpResponseRedirect(url)
