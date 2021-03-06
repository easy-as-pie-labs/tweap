from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import View
from notification_center.models import Notification
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import json


class ViewAll(View):
    def get(self, request):
        notifications = Notification.objects.filter(receiver=request.user)
        return render(request, 'notification_center/view_all.html', {'notifications': notifications})


class ViewOne(View):
    def get(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            url = notification.target_url
            if request.user == notification.receiver:
                notification.delete()
            else:
                return HttpResponseRedirect(reverse('dashboard:home'))
        except Notification.DoesNotExist:
            return HttpResponseRedirect(reverse('dashboard:home'))
        return HttpResponseRedirect(url)


class MarkSeen(View):
    def post(self, request):

        notification_id = request.POST.get('notificationId', '')
        try:
            notification = Notification.objects.get(id=notification_id)
            if request.user == notification.receiver:
                notification.delete()
            else:
                return HttpResponseRedirect(reverse('dashboard:home'))
            result = {'state': True}
        except Notification.DoesNotExist:
            result = {'state': True}

        return HttpResponse(json.dumps(result), content_type="application/json")


class MarkAllSeen(View):
    def post(self, request):
        try:
            Notification.objects.filter(receiver=request.user).delete()
            result = {'success': True}
        except:
            result = {'success': False}

        return HttpResponse(json.dumps(result), content_type="application/json")
