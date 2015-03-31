from django.shortcuts import render
from django.views.generic import View
from project_management.models import Invitation
from notification_center.models import Notification
from todo.models import Todo
from cal.models import Event
import datetime


class Home(View):
    """
    View function for the home
    """
    def get(self, request):
        if request.user.is_authenticated():

            todo_week = Todo.get_due_this_week_for_user(request.user)

            cal_today = Event.get_start_today_for_user(request.user)
            for entry in cal_today:
                entry.start = entry.get_start_time_for_dashboard()

            cal_week = Event.get_start_this_week_for_user(request.user)

            # mix week todos and events so that they can be sorted by date and not be in seperate categories
            week_events_todos = []
            todos = list(todo_week.all())
            for todo in todos:
                todo.type = 'todo'
                todo.timestamp = todo.get_date_for_dashboard()
            events = list(cal_week.all())
            for event in events:
                event.type = 'event'
                event.timestamp = event.get_start_datetime_for_dashboard()
            while True:
                if len(todos) > 0 and len(events) > 0:
                    if (todos[0].due_date.year == events[0].start.year and todos[0].due_date.month == events[0].start.month and todos[0].due_date.day < events[0].start.day) \
                            or (todos[0].due_date.month < events[0].start.month) \
                            or (todos[0].due_date.year < events[0].start.year):
                        week_events_todos.append(todos[0])
                        del todos[0]
                    else:
                        week_events_todos.append(events[0])
                        del events[0]
                else:
                    for todo in todos:
                        week_events_todos.append(todo)
                    for event in events:
                        week_events_todos.append(event)
                    break


            context = {
                'invitations': Invitation.objects.filter(user=request.user),
                'due_today': Todo.get_due_today_for_user(request.user),
                'overdue': Todo.get_overdue_for_user(request.user),
                'events_today': cal_today,
                'notifications': Notification.objects.filter(receiver=request.user),
                'week_mixed': week_events_todos
            }
            return render(request, 'dashboard/dashboard.html', context)
        else:
            return render(request, 'dashboard/home.html')
