from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from project_management.models import ProjectForm, Project as ProjectModel, Invitation
from project_management.tools import invite_users


class Create(View):
    """
    View class for creating a new project
    """
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


class Edit(View):
    """
    View class for editing an existing project
    """
    def get(self, request, project_id=None):
        project = get_object_or_404(ProjectModel, id=project_id)
        if request.user in project.members.all():
            context = {
                'form': ProjectForm(instance=project),
                'project': project,
                'members': project.members.all(),
                'invitations': Invitation.objects.filter(project=project)
            }

            return render(request, 'project_management/edit.html', context)
        else:
            raise Http404

    def post(self, request, project_id=None):
        project = get_object_or_404(ProjectModel, id=project_id)
        if request.user in project.members.all():
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('project_management:project', args=(project.id, )))
            else:
                context = {'error_messages': form.errors, 'form': form, 'project': project}
                return render(request, 'project_management/edit.html', context)
        else:
            raise Http404



class Project(View):
    """
    View class for viewwing a project
    """
    def get(self, request, project_id=None):
        context = {}
        project = get_object_or_404(ProjectModel, id=project_id)
        context['project'] = project
        context['members'] = project.members.all()
        context['invitations'] = Invitation.objects.filter(project=project)
        if request.user in context['members']:
            return render(request, 'project_management/project.html', context)
        else:
            raise Http404

class ViewAll(View):
    """
    View class for displaying all projects of an user
    """
    def get(self, request):
        context = {'projects': ProjectModel.objects.filter(members=request.user.id)}
        return render(request, 'project_management/view_all.html', context)


def view_invites(request):
    """
    View function for displaying all invitations of an user
    :param request:
    :return:
    """
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
