from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext
from django.contrib.auth.models import User
from project_management.models import Project
from project_management.tools import get_tags, make_tag
from notification_center.models import NotificationEvent, Notification
from todo.tools import *
from tweap.tools import StringParser
import json
import datetime
from django.core import serializers


class CreateEdit(View):
    """
    View class for creating or editing a todo
    """
    def get(self, request, todo_id=None, project_id=None):

        if todo_id is None:
            if project_id is None:
                raise Http404

            project = get_object_or_404(Project, id=project_id)

            project_members = project.members.all()

            # redirect if user is not in group at all
            if request.user not in project_members:
                raise Http404

            context = {
                'headline': ugettext("Create new Todo in") + " " + project.name,
                'project': project,
                'members': project.members.order_by('username'),
                'invitees': project.get_invited_users()
            }

            return render(request, 'todo/create_edit.html', context)

        todo = get_object_or_404(Todo, id=todo_id)

        project = todo.project

        # redirect if user is not in group at all
        if request.user not in project.members.all():
            raise Http404
        else:
            context = {
                'headline': ugettext("Edit Todo in") + " " + project.name,
                'todo': todo,
                'project': project,
                'members': project.members.order_by('username'),
            }
        return render(request, 'todo/create_edit.html', context)

    def post(self, request, todo_id=None, project_id=None):

        form = request.POST

        if todo_id is None:
            if project_id is None:
                raise Http404

            todo = Todo()
            project = get_object_or_404(Project, id=project_id)
            project_members = project.members.all()

            # redirect if user is not in group at all
            if request.user not in project_members:
                raise Http404

        else:
            todo = get_object_or_404(Todo, id=todo_id)
            project = todo.project
            project_members = project.members.all()

            # redirect if user is not in group at all
            if request.user not in project_members:
                raise Http404

        if 'title' in form:
            if form['title'] != "":
                todo.title = form['title']
                todo.description = form['description']

                due_date = form['due_date']
                if due_date == '':
                    todo.due_date = None
                else:
                    todo.due_date = due_date

                todo.project = project
                assignees = form.getlist('assignees')
                todo.save()

                # only get assignees that weren't assigned before (for notifications)
                not_yet_assigned = []

                for assignee in assignees:
                    user = User.objects.get(username=assignee)
                    if user not in todo.assignees.all():
                        not_yet_assigned.append(user)

                todo.assignees.clear()
                for assignee in assignees:
                    user = User.objects.get(username=assignee)
                    # if the post data was manipulated and a user assigned who is not in the project let's ignore it
                    if user in project.members.all():
                        todo.assignees.add(user)

                todo.tags.clear()
                tags = get_tags(form['tags'], todo.project)
                for tag in tags:
                    todo.tags.add(tag)

                todo.save()

                # create notifications for all assignees
                Notification.bulk_create(not_yet_assigned, request.user, project, request.build_absolute_uri(reverse('todo:edit', args=(todo.id, ))), 'assigned a todo to you')

                return HttpResponseRedirect(reverse('project_management:project', args=(project.id, )))

        context = {}
        context['error_messages'] = {'name': ugettext("Invalid Entry")}
        context['project'] = project
        if todo_id is not None:
            context['todo'] = todo
            context['headline'] = ugettext("Edit Todo in") + " " + project.name
        else:
            context['headline'] = ugettext("Create new Todo in") + " " + project.name
        return render(request, 'todo/create_edit.html', context)

class Delete(View):
    def get(self, request, todo_id):

        todo = validate_for_todo(request, todo_id)
        target_url = request.build_absolute_uri(reverse('todo:edit', args=(todo.id, )))
        Notification.objects.filter(target_url=target_url).delete()
        todo.delete()

        return HttpResponseRedirect(reverse('project_management:project', args=(todo.project.id, )))

    def post(self, request, todo_id):

        todo = validate_for_todo(request, todo_id)
        target_url = request.build_absolute_uri(reverse('todo:edit', args=(todo.id, )))
        Notification.objects.filter(target_url=target_url).delete()
        todo.delete()

        return HttpResponseRedirect(reverse('project_management:project', args=(todo.project.id, )))


class MarkDone(View):
    def post(self, request):

        todo_id = request.POST.get('todo_id', '')

        todo = validate_for_todo(request, todo_id)
        todo.done = True
        todo.completed_date = datetime.datetime.today()
        todo.save()
        result = {'state': True}

        return HttpResponse(json.dumps(result), content_type="application/json")



class MarkUndone(View):
    def post(self, request):

        todo_id = request.POST.get('todo_id', '')

        todo = validate_for_todo(request, todo_id)
        todo.done = False
        todo.completed_date = None
        todo.save()
        result = {'state': True}

        return HttpResponse(json.dumps(result), content_type="application/json")


class QuickAdd(View):
    def post(self, request):
        project_id = int(request.POST.get('project_id', ''))
        text = request.POST.get('title', '')

        sp = StringParser({'@': 'users', '#': 'tags'}, 'title')
        data = sp.parse(text)

        title = data['title']

        result = {}
        try:
            project = Project.objects.get(id=project_id)
            todo = Todo(project=project, title=title, description='')
            todo.save()

            for username in data['users']:
                try:
                    user = User.objects.get(username=username)

                    if user in project.members.all():
                        todo.assignees.add(user)
                except:
                    pass

            for tag in data['tags']:
                try:
                    todo.tags.add(make_tag(tag, project))
                except:
                    pass

            todo.save()

            if title == '':
                todo.delete()
                raise Exception

            tags = todo.tags.all().only('name')
            tags_list = []
            for tag in tags:
                tags_list.append(tag.name)

            assignees = todo.assignees.all().only('username')

            if len(assignees) == 0:
                assignment = 'none'
            elif request.user in assignees:
                assignment = 'you'
            else:
                assignment = 'someone'

            assignee_list = []
            for assignee in assignees:
                assignee_list.append(assignee.username)

            Notification.bulk_create(assignees, request.user, project, request.build_absolute_uri(reverse('todo:edit', args=(todo.id, ))), 'assigned a todo to you')
            result = {'success': True, 'id': todo.id, 'title': todo.title, 'tags': tags_list, 'users': assignee_list, 'assignment': assignment}
        except:
            result = {'success': False}

        return HttpResponse(json.dumps(result), content_type="application/json")


class QuickAssign(View):
    def post(self, request):
        todo_id = int(request.POST.get('todo_id', ''))
        user = request.user
        todo = Todo.objects.get(id=todo_id)
        todo.assignees.add(user)
        todo.save()

        tags = todo.tags.all().only('name')
        tags_list = []
        for tag in tags:
            tags_list.append(tag.name)

        assignees = todo.assignees.all().only('username')

        if len(assignees) == 0:
            assignment = 'none'
        elif request.user in assignees:
            assignment = 'you'
        else:
            assignment = 'someone'

        assignee_list = []
        for assignee in assignees:
            assignee_list.append(assignee.username)

        result = {'success': True, 'id': todo.id, 'title': todo.title, 'tags': tags_list, 'users': assignee_list, 'assignment': assignment}
        try:
            due_date = todo.due_date
            if due_date is not None:
                result['year'] = todo.due_date.year
                result['month'] = todo.due_date.month
                result['day'] = todo.due_date.day
        except:
            pass

        return HttpResponse(json.dumps(result), content_type="application/json")


class QuickUnAssign(View):
    def post(self, request):
        todo_id = int(request.POST.get('todo_id', ''))
        user = request.user
        todo = Todo.objects.get(id=todo_id)
        todo.assignees.remove(user)
        todo.save()

        tags = todo.tags.all().only('name')
        tags_list = []
        for tag in tags:
            tags_list.append(tag.name)

        assignees = todo.assignees.all().only('username')

        if len(assignees) == 0:
            assignment = 'none'
        elif request.user in assignees:
            assignment = 'you'
        else:
            assignment = 'someone'

        assignee_list = []
        for assignee in assignees:
            assignee_list.append(assignee.username)

        result = {'success': True, 'id': todo.id, 'title': todo.title, 'tags': tags_list, 'users': assignee_list, 'assignment': assignment}
        try:
            due_date = todo.due_date
            if due_date is not None:
                result['year'] = todo.due_date.year
                result['month'] = todo.due_date.month
                result['day'] = todo.due_date.day
        except:
            pass

        return HttpResponse(json.dumps(result), content_type="application/json")