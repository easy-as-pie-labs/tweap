from django.shortcuts import render
from django.views.generic import View
from project_management.models import Invitation
from notification_center.models import Notification
from todo.models import Todo
from cal.models import Event


class Home(View):
    """
    View function for the home
    """
    def get(self, request):
        if request.user.is_authenticated():

            cal_today = Event.get_due_today_for_user(request.user)

            for entry in cal_today:
                entry.start = entry.get_start_time_for_dashboard()

            context = {
                'invitations': Invitation.objects.filter(user=request.user),
                'due_today': Todo.get_due_today_for_user(request.user),
                'due_this_week': Todo.get_due_this_week_for_user(request.user),
                'overdue': Todo.get_overdue_for_user(request.user),
                'events_today': cal_today,
                'events_this_week': Event.get_due_this_week_for_user(request.user),
                'notifications': Notification.objects.filter(receiver=request.user)
            }
            return render(request, 'dashboard/dashboard.html', context)
        else:
            return render(request, 'dashboard/home.html')
