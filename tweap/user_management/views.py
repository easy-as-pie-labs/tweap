from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from user_management.tools import validate_registration_form, register_and_login


class Register(View):

    def get(self, request):
        return render(request, 'user_management/register.html', {})

    def post(self, request):
        credentials, errors = validate_registration_form(request.POST)
        if not errors:
            register_and_login(credentials, request)
            return HttpResponseRedirect(reverse('user_management:home'))  # TODO: hier zum Dashbord directen
        else:
            context = {'error_messages': errors}
            if 'username' not in errors:
                context['username'] = credentials['username']
            if 'username' not in errors:
                context['email'] = credentials['email']
            return render(request, 'user_management/register.html', context)


class Home(View):
    def get(self, request):
        return HttpResponse("Home")
