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

            todo_week = Todo.get_due_this_week_for_user(request.user)
            for entry in todo_week:
                entry.due_date = entry.get_date_for_dashboard()

            cal_today = Event.get_start_today_for_user(request.user)
            for entry in cal_today:
                entry.start = entry.get_start_time_for_dashboard()

            cal_week = Event.get_start_this_week_for_user(request.user)
            for entry in cal_week:
                entry.start = entry.get_start_datetime_for_dashboard()


            context = {
                'invitations': Invitation.objects.filter(user=request.user),
                'due_today': Todo.get_due_today_for_user(request.user),
                'due_this_week': todo_week,
                'overdue': Todo.get_overdue_for_user(request.user),
                'events_today': cal_today,
                'events_this_week': cal_week,
                'notifications': Notification.objects.filter(receiver=request.user)
            }
            return render(request, 'dashboard/dashboard.html', context)
        else:
            return render(request, 'dashboard/home.html')
