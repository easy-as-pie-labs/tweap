from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from project_management.models import ProjectForm
from project_management.tools import invite_users


class Create(View):

    def get(self, request):
        form = ProjectForm()
        context = {'form': form}
        return render(request, 'project_management/create.html', context)

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.members.add(request.user)
            project.save()
            if 'invitations' in request.POST:
                invite_users(request.POST['invitations'])
            return HttpResponseRedirect(reverse('project_management:project'))
        else:
            context = {'error_messages': form.errors, 'form': form}
            return render(request, 'project_management/create.html', context)
