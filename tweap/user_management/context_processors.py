from project_management.models import Invitation


def user_info(request):
    no_of_invites = ""
    if request.user.is_authenticated():
        no_of_invites = Invitation.objects.filter(user=request.user.id).count()

    return {
        'no_of_invites': no_of_invites,
    }
