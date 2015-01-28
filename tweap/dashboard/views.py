from django.shortcuts import render
from django.views.generic import View


class Home(View):
    """
    View function for the home
    """
    def get(self, request):
        if request.user.is_authenticated():
            return render(request, 'dashboard/dashboard.html', {})
        else:
            return render(request, 'dashboard/home.html')
