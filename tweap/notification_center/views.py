from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from notification_center.models import Notification
from django.core.urlresolvers import reverse
import json


class ViewAll(View):
    def get(self, request):
        notifications = Notification.objects.filter(receiver=request.user)

        return render(request, 'notification_center/view_all.html', {'notifications': notifications})


class ViewOne(View):
    def get(self, request, notification_id):
        # TODO: error handling
        try:
            notification = Notification.objects.get(id=notification_id)
            url = notification.target_url
            notification.delete()
        except Notification.DoesNotExist:
            return HttpResponseRedirect(reverse('dashboard:home'))
        return HttpResponseRedirect(url)


class MarkSeen(View):
    def post(self, request):

        notification_id = request.POST.get('notificationId', '')
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            result = {'state': True}
        except Notification.DoesNotExist:
            result = {'state': True}

        return HttpResponse(json.dumps(result), content_type="application/json")
