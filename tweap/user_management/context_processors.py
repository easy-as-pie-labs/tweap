from project_management.models import Project


def user_info(request):
    projects = None
    if request.user.is_authenticated():
        projects = Project.objects.filter(members=request.user)

    return {
        'username': request.user.username,
        'projects': projects
    }
