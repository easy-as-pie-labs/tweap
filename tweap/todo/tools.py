from django.shortcuts import get_object_or_404
from todo.models import Todo
from django.http import Http404

def validate_for_todo(request, todo_id):

    todo = get_object_or_404(Todo, id=todo_id)
    project = todo.project

    if request.user not in project.members.all():
        raise Http404
    return todo
