from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext
from todo.models import Todo
from django.contrib.auth.models import User
from project_management.models import Project
from project_management.tools import get_tags
from notification_center.models import Event, Notification


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

        project_members = project.members.all()

        tags = todo.tags.all()

        # redirect if user is not in group at all
        if request.user not in project_members:
            raise Http404
        else:
            context = {
                'headline': ugettext("Edit Todo"),
                'todo': todo,
                'tags': tags,
                'members': project_members,
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

                # see if event type already exists in db
                event_text = "assigned a todo to you"
                try:
                    event = Event.objects.get(text=event_text)
                except:
                    event = Event()
                    event.text = event_text
                    event.save()

                # send out notifications
                for assignee in assignees:
                    user = User.objects.get(username=assignee)

                    # We don't want a notification for the user who created this
                    # also if the post data was manipulated and a user assigned who is not in the project let's ignore it
                    if user == request.user or user not in project.members.all():
                        continue

                    notification = Notification()
                    notification.receiver = user
                    notification.trigger_user = request.user
                    notification.project = project
                    notification.target_url = request.build_absolute_uri(reverse('todo:edit', args=(todo.id, )))
                    notification.event = event
                    notification.save()

                return HttpResponseRedirect(reverse('project_management:project', args=(project.id, )))

        context = {
            'error_messages': {'name': ugettext("The title must not be empty!")},
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

    def post(self, request, todo_id):
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

