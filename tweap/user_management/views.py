from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import logout as django_logout
from user_management.models import ProfileAddress, PostalCode
from user_management.tools import validate_registration_form, register_and_login, login
from django.utils.translation import ugettext
from django.contrib.auth.models import User


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
            if 'form' not in errors:
                if 'username' not in errors:
                    context['username'] = credentials['username']
                if 'email' not in errors:
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
            context['error_message'] = ugettext("Login not successful!")
            return render(request, 'user_management/login.html', context)


def logout(request):
    django_logout(request)
    context = {'redirect': request.GET.get('next', '')}
    return render(request, 'user_management/logout.html', context)


class Home(View):
    def get(self, request):
        if request.user.is_authenticated():
            welcome_message = ugettext("Home! Hello User!")
        else:
            welcome_message = ugettext("Home! Hello Guest!")
        return HttpResponse(welcome_message)


class ViewProfile(View):
    def get(self, request, user_id = None):
        if user_id == None:
            user_id = request.user.id
        user_data = get_object_or_404(User, id=user_id)
        profile_address_data = ProfileAddress.objects.get(id=user_data.profile.id)
        postal_code_data = PostalCode.objects.get(id=profile_address_data.id)
        context = {'user_data': user_data, 'profile_address_data': profile_address_data, 'postal_code_data': postal_code_data}
        return render(request, 'user_management/profile.html', context)
