from django.shortcuts import render
from django.views.generic import View
from project_management.models import Invitation
from todo.models import Todo

class Home(View):
    """
    View function for the home
    """
    def get(self, request):
        if request.user.is_authenticated():
            context = {
                'invitations': Invitation.objects.filter(user=request.user),
                'due_today': Todo.get_due_today_for_user(request.user),
                'due_this_week': Todo.get_due_this_week_for_user(request.user),
                'overdue': Todo.get_overdue_for_user(request.user),
            }
            return render(request, 'dashboard/dashboard.html', context)
        else:
            return render(request, 'dashboard/home.html')
