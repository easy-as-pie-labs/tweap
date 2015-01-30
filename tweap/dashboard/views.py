from django.shortcuts import render
from django.views.generic import View
from project_management.models import Invitation

class Home(View):
    """
    View function for the home
    """
    def get(self, request):
        if request.user.is_authenticated():
            invitation_count = Invitation.objects.filter(user=request.user).count()
            return render(request, 'dashboard/dashboard.html', {'invitation_count': invitation_count})
        else:
            return render(request, 'dashboard/home.html')
