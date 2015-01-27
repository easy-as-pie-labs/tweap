from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from project_management.models import ProjectForm, Project as ProjectModel, Invitation
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
                invite_users(request.POST['invitations'], project)
            return HttpResponseRedirect(reverse('project_management:project', args=(project.id, )))
        else:
            context = {'error_messages': form.errors, 'form': form}
            return render(request, 'project_management/create.html', context)


class Project(View):

    def get(self, request, project_id=None):
        context = {}
        project = get_object_or_404(ProjectModel, id=project_id)
        context['project'] = project
        context['members'] = project.members.all()
        context['invitations'] = Invitation.objects.filter(project=project)
        if ProjectModel.objects.filter(members=request.user.id, id=project.id):
            return render(request, 'project_management/project.html', context)
        else:
            raise Http404

class ViewAll(View):
    def get(self, request):
        context = {'projects': ProjectModel.objects.filter(members=request.user.id)}
        return render(request, 'project_management/view_all.html', context)


def view_invites(request):
    invites = Invitation.objects.filter(user=request.user.id)
    projects = []
    for invite in invites:
        projects.append(ProjectModel.objects.get(id=invite.project.id))
    context = {'projects': projects}
    return render(request, 'project_management/view_invites.html', context)


def leave_group(request, project_id):
    project = ProjectModel.objects.get(id=project_id)
    project.leave(request.user)

    #TODO: this isn't OK
    return redirect('../all', permanent=True)


def accept_invite(request, project_id):
    project = ProjectModel.objects.get(id=project_id)
    invitation = Invitation.objects.get(user=request.user, project=project)
    invitation.accept()

    #TODO: this isn't OK
    return redirect('../all', permanent=True)


def reject_invite(request, project_id):
    project = ProjectModel.objects.get(id=project_id)
    invitation = Invitation.objects.get(user=request.user, project=project)
    invitation.reject()

    #TODO: this isn't OK
    return redirect('../invites', permanent=True)
