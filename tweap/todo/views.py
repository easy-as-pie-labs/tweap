from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext
from todo.models import Todo
from django.contrib.auth.models import User
from project_management.models import Project
from project_management.tools import get_tags


class CreateEdit(View):
    """
    View class for creating or editing a todo
    """
    def get(self, request, todo_id=None, project_id=None):

        if todo_id is None:
            if project_id is None:
                raise Http404

            project = Project.objects.get(id=project_id)
            context = {
                'headline': ugettext("Create new Todo"),
                'project': project,
                'members': project.members.all(),
            }

            return render(request, 'todo/create_edit.html', context)

        todo = get_object_or_404(Todo, id=todo_id)

        if project_id is None:
            project = todo.project
        else:
            project = Project.objects.get(project_id)

        assigned_users = project.members.all()
        tags = todo.tags.all()
        if request.user not in assigned_users:
            raise Http404
        else:
            context = {
                'headline': ugettext("Edit Todo"),
                'todo': todo,
                'tags': tags,
                'members': assigned_users,
                'project': project,
                'date': todo.get_date(),
                'assignees': todo.assignees.all(),
            }
        return render(request, 'todo/create_edit.html', context)

    def post(self, request, todo_id=None, project_id=None):

        form = request.POST

        if todo_id is None:
            if project_id is None:
                raise Http404

            todo = Todo()
            project = Project.objects.get(id=project_id)

        else:
            todo = get_object_or_404(Todo, id=todo_id)
            project = todo.project
            assigned_users = project.members.all()
            if request.user not in assigned_users:
                raise Http404

        if 'title' in form:
            todo.title = form['title']
            todo.description = form['description']

            due_date = form['due_date']
            if due_date != '':
                todo.due_date = due_date

            todo.project = project
            assignees = form.getlist('assignees')
            todo.save()
            todo.clear_assignees()
            for assignee in assignees:
                todo.assignees.add(User.objects.get(username=assignee))
            tags = get_tags(form['tags'], todo.project)

            for tag in tags:
                todo.tags.add(tag)

            todo.save()
            return HttpResponseRedirect(reverse('project_management:project', args=(project.id, )))

        project = Project.objects.get(id=project_id)
        context = {
            'error_messages': {'name': ugettext("The name must not be empty!")},
            'project': project,
            'members': project.members.all(),
            'headline': ugettext("Create new Todo"),
            'date': todo.get_date(),
        }
        return render(request, 'todo/create_edit.html', context)


class Delete(View):
    def get(self, request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return HttpResponseRedirect(reverse('project_management:project', args=(todo.project.id, )))


class MarkDone(View):
    def get(self, request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        todo.done = True
        todo.save()
        return HttpResponseRedirect(reverse('project_management:project', args=(todo.project.id, )))


class MarkUndone(View):
    def get(self, request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        todo.done = False
        todo.save()
        return HttpResponseRedirect(reverse('project_management:project', args=(todo.project.id, )))

