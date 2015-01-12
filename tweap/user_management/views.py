from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib.auth.models import User as UserModel
from django.contrib.auth import authenticate, login
from user_management.tools import validate_registration_form


class Register(View):

    def get(self, request):
        return render(request, 'user_management/register.html', {})

    def post(self, request):
        context = {}
        if 'username' in request.POST and 'email' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password = str(request.POST['password'])
            context['error_messages'] = validate_registration_form(username, email, password)
            if not context['error_messages']:
                UserModel.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('user_management:home'))  #TODO: hier zum Dashbord directen

            if 'username' not in context['error_messages']:
                context['username'] = username
            if 'email' not in context['error_messages']:
                context['email'] = email

        return render(request, 'user_management/register.html', context)


class Home(View):
    def get(self, request):
        return HttpResponse("Home")
