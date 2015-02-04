from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext
from todo.models import Todo
from django.contrib.auth.models import User
from project_management.models import Project


class CreateEdit(View):
    """
    View class for creating of editing a project
    """

    def get(self, request, todo_id=None, project_id=None):
        if todo_id is None:
            project = Project.objects.get(id=project_id)
            context = {
                'headline': ugettext("Create new ToDo"),
                'project': project,
                'members': project.members.all(),
            }

        else:
            todo = get_object_or_404(Todo, id=todo_id)
            project = todo.project
            assigned_users = project.members.all()
            tags = todo.tags
            if request.user not in assigned_users:
                raise Http404
            else:
                context = {
                    'headline': ugettext("Edit Todo"),
                    'todo': todo,
                    'tags': tags,
                    'members': assigned_users,
                    'project': project
                }
        return render(request, 'todo/create_edit.html', context)

    def post(self, request, todo_id=None, project_id=None):

        context = {}
        form = request.POST

        if todo_id is None:
                if project_id is None:
                    context['headline'] = ugettext("Create new ToDo")
                    render(request, 'todo/create_edit', context)
                else:
                    todo = Todo()
        else:
            todo = get_object_or_404(Todo, id=todo_id)
            project = todo.project
            assigned_users = project.members.all()
            if request.user not in assigned_users:
                raise Http404
        if 'title' in form:
            todo.title = form['title']
            todo.description = form['description']
            todo.due_date = form['due_date']
            todo.project = Project.objects.filter(id=project_id)
            assignees = form.getlist('assignees')

            for assignee in assignees:
                todo.assignees.add(User.objects.filter(username=assignee))
            #Todo: Search for tags and save them
            todo.save()
            return HttpResponse(reverse('project_management:project', args=(project.id, )))
        else:
            context['error_messages'] = [ugettext("The title must not be empty!")]
            return render(request, 'todo/create_edit', context)


