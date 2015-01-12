from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User as UserModel
from django.contrib.auth import authenticate, login


class Register(View):
    bad_passwords = ('123', ) #TODO: füllen!

    def get(self, request):
        context = {}
        return render(request, 'user_management/register.html', context)

    def post(self, request):
        context = {}
        if 'username' in request.POST and 'email' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            context['username'] = username
            context['email'] = email
            if username is not (None or "") and email is not (None or "") and password is not (None or ""):
                context['error_messages'] = {}
                if UserModel.objects.filter(username=username).exists():
                    context['error_messages']['username'] = "Benutzername ist nicht verfügbar" #TODO: lokalisierung
                    context.pop('username')
                if UserModel.objects.filter(email=email).exists():
                    context['error_messages']['email'] = "E-Mail-Adresse wird bereits für einen anderen Account verwendet" #TODO: lokalisierung
                    context.pop('email')
                if password in self.bad_passwords:
                    context['error_messages']['password'] = "Lol!" #TODO: lokalisierung und Text

                if context['error_messages']:
                    return render(request, 'user_management/register.html', context)

                UserModel.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return render(request, 'user_management/home.html', context)
            else:
                return render(request, 'user_management/register.html', context)
        else:
            return render(request, 'user_management/register.html', context)


