from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import logout as django_logout
from user_management.tools import validate_registration_form, register_and_login, login


class Register(View):

    def get(self, request):
        return render(request, 'user_management/register.html', {})

    def post(self, request):
        credentials, errors = validate_registration_form(request.POST)
        if not errors:
            register_and_login(credentials, request)
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
        else:
            context = {'error_messages': errors}
            if 'username' not in errors:
                context['username'] = credentials['username']
            if 'username' not in errors:
                context['email'] = credentials['email']
            return render(request, 'user_management/register.html', context)


class Login(View):
    def get(self, request):
        context = {'redirect': request.GET.get('next', '')}
        return render(request, 'user_management/login.html', context)

    def post(self, request):
        redirect = request.POST.get('next', '')
        if not redirect:
            redirect = reverse(settings.LOGIN_REDIRECT_URL)
        context = {'redirect': redirect}
        username = str(request.POST.get('username', '')).strip().lower()
        password = str(request.POST.get('password', '')).strip()
        if login(username, password, request):
            return HttpResponseRedirect(redirect)
        else:
            context['error_message'] = "Login nicht erfolgreich."
            return render(request, 'user_management/login.html', context)


def logout(request):
    django_logout(request)
    return HttpResponse("Erfolgreich ausgeloggt!")  # TODO: template erstellen und rendern


class Home(View):
    def get(self, request):
        if request.user.is_authenticated():
            welcome_message = "User"
        else:
            welcome_message = "Gast"
        return HttpResponse("Home! Hallo " + welcome_message)

