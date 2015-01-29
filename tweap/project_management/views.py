from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from project_management.models import ProjectForm, Project as ProjectModel, Invitation
from project_management.tools import invite_users
import json


class CreateEdit(View):
    """
    View class for creating or editing a project
    """

    def get(self, request, project_id=None):

        if project_id is None:
            context = {
                'form': ProjectForm(),
                'headline': ugettext("Create new project")
            }

        else:
            project = get_object_or_404(ProjectModel, id=project_id)
            if request.user not in project.members.all():
                raise Http404
            else:
                context = {
                    'form': ProjectForm(instance=project),
                    'headline': ugettext("Edit project"),
                    'project': project,
                    'members': project.members.all(),
                    'invitations': Invitation.objects.filter(project=project)
                }

        return render(request, 'project_management/create_edit.html', context)



    def post(self, request, project_id=None):

        context = {}

        if project_id is None:
            form = ProjectForm(request.POST)
            context['headline'] = ugettext("Create new project")

        else:
            project = get_object_or_404(ProjectModel, id=project_id)
            if request.user not in project.members.all():
                raise Http404
            else:
                form = ProjectForm(request.POST, instance=project)
                context['headline'] = ugettext("Edit project")
                context['project'] = project

        if form.is_valid():
            project = form.save()
            if project_id is None:
                project.members.add(request.user)
                project.save()
            if 'invitations' in request.POST:
                invite_users(request.POST['invitations'], project)
            return HttpResponseRedirect(reverse('project_management:project', args=(project.id, )))

        else:
            context['error_messages'] = form.errors
            context['form'] = form
            return render(request, 'project_management/create_edit.html', context)


class Project(View):
    """
    View class for viewing a project
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
        context = {'projects': ProjectModel.objects.filter(members=request.user)}
        return render(request, 'project_management/view_all.html', context)


def view_invites(request):
    """
    View function for displaying all invitations of an user
    :param request:
    :return:
    """
    invitations = Invitation.objects.filter(user=request.user)
    context = {'invitations': invitations}
    return render(request, 'project_management/view_invites.html', context)


def leave(request):
    """
    view function for leaving a project
    :param request:
    :return:
    """
    if request.method == 'POST':
        project_id = request.POST.get('project_id', '')
        if project_id:
            project = get_object_or_404(ProjectModel, id=project_id)
            if request.user in project.members.all():
                project.leave(request.user)
                return HttpResponseRedirect(reverse('project_management:view_all'))
    # TODO: wenn letzter user leaved im frontend auf das aut. löschen der gruppe hinweisen
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def invitation_handler(request):
    """
    view function for handling invitation actions (accept, reject)
    :param request:
    :return:
    """
    result = {'message': 'An error occured', 'url': ''}
    if request.method == 'POST':
        invitation_id = request.POST.get('invitation_id', '')
        action = request.POST.get('action', '')
        if invitation_id:
            invitation = Invitation.objects.get(id=invitation_id)
            if invitation.user == request.user:
                if action == 'accept':
                    invitation.accept()
                    result['message'] = ugettext("Invitation was accepted")
                    result['url'] = reverse('project_management:project', args=(invitation.project.id,))
                if action == 'reject':
                    invitation.reject()
                    result['message'] = ugettext("Invitation was rejected")

    return HttpResponse(json.dumps(result), content_type="application/json")


def accept_invite(request, project_id):
    project = ProjectModel.objects.get(id=project_id)
    invitation = Invitation.objects.get(user=request.user, project=project)
    invitation.accept()

    #TODO: this isn't OK
    return redirect('../' + str(project_id), permanent=True)


def reject_invite(request, project_id):
    project = ProjectModel.objects.get(id=project_id)
    invitation = Invitation.objects.get(user=request.user, project=project)
    invitation.reject()

    #TODO: this isn't OK
    return redirect('../invites', permanent=True)
