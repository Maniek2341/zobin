from modules.users.models import PanelUser, UsersProfile


def base_realated_variable(request):
    if (request.user.id):
        profile = UsersProfile.objects.get(user=request.user)
        return {
            'user': profile
        }
    return {}