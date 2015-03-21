from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext
from project_management.models import ProjectForm, Project, Invitation, Tag
from project_management.tools import invite_users
from todo.models import Todo
from cal.models import Event
import datetime
import pytz
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
            project = get_object_or_404(Project, id=project_id)
            if request.user not in project.members.all():
                raise Http404
            else:
                context = {
                    'form': ProjectForm(instance=project),
                    'headline': ugettext("Edit project"),
                    'project': project,
                    'invitations': Invitation.objects.filter(project=project)
                }

        return render(request, 'project_management/create_edit.html', context)

    def post(self, request, project_id=None):

        context = {}

        if project_id is None:
            form = ProjectForm(request.POST)
            context['headline'] = ugettext("Create new project")

        else:
            project = get_object_or_404(Project, id=project_id)
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


class ProjectView(View):
    """
    View class for viewing a project
    """
    def get(self, request, project_id=None):
        context = {}
        project = get_object_or_404(Project, id=project_id)
        context['project'] = project
        context['invitations'] = Invitation.objects.filter(project=project)

        overdue = Todo.get_open_overdue_for_project(project)
        today = Todo.get_open_due_today_for_project(project)
        closed = Todo.get_closed_for_project(project)
        rest = Todo.get_open_rest_for_project(project)

        context['todo_overdue'] = self.mark_todo_assignment(overdue, request.user)
        context['todo_today'] = self.mark_todo_assignment(today, request.user)
        context['todo_closed'] = self.mark_todo_assignment(closed, request.user)
        context['todo_rest'] = self.mark_todo_assignment(rest, request.user)

        context['events'] = Event.get_all_for_project(project)
        context['members'] = project.members.order_by('username')

        future = []
        past = []

        for event in context['events']:
            if datetime.datetime.now(pytz.utc) <= event.start:
                future.append(event)
            else:
                past.append(event)

        context['future'] = future
        context['past'] = past[-5:][::-1] # only shows 5 past entries, in descending date order

        members = project.members.all()
        if request.user in members:
            return render(request, 'project_management/project.html', context)
        else:
            raise Http404

    @classmethod
    def mark_todo_assignment(cls, queryset, user):
        """
        adds assignment field to todos in queryset,
        so that we now who is working on a todo
        (for frontend usage)
        :param queryset: queryset of todos
        :param user: user to check assignment for
        :return: queryset of todos
        """
        for todo in queryset:
            assignees = todo.assignees.all()
            if len(assignees) == 0:
                todo.assignment = 'none'
            elif user in assignees:
                todo.assignment = 'you'
            else:
                todo.assignment = 'someone'

        return queryset

class LeaveGroup(View):
    """
    view class for leaving a project
    :param request:
    :return:
    """
    def post(self, request):
        project_id = request.POST.get('project_id', '')
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            if request.user in project.members.all():
                project.leave(request.user)
                return HttpResponseRedirect(reverse('dashboard:home'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class InvitationHandler(View):
    """
    view function for handling invitation actions (accept, reject)
    :param request:
    :return:
    """
    def post(self, request):
        result = {'url': '', 'id': ''}
        invitation_id = request.POST.get('invitation_id', '')
        action = request.POST.get('action', '')
        if invitation_id:
            invitation = Invitation.objects.get(id=invitation_id)
            if invitation.user == request.user:
                if action == 'accept':
                    invitation.accept()
                    result['url'] = request.build_absolute_uri(reverse('project_management:project', args=(invitation.project.id,)))
                if action == 'reject':
                    invitation.reject()

        return HttpResponse(json.dumps(result), content_type="application/json")


class TagSuggestion(View):
    """
    view function for searching tags in a project
    :param request:
    :return: list of tags as JSON string
    """
    def get(self, request):
        result = []
        search = request.GET.get('search', '')
        if search:
            project_id = request.GET.get('project_id', '')
            if project_id:
                tags = Tag.objects.filter(project__id=project_id, name__istartswith=search)[:5]
                for tag in tags:
                    result.append(tag.name)
        return HttpResponse(json.dumps(result), content_type="application/json")
