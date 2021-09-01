import datetime

from modules.users.models import PanelUser


def base_realated_variable(request):
    if request.user.id:
        profile = PanelUser.objects.get(username=request.user.username)
        return {
            'prof': profile,
            'rok': datetime.date.today().year
        }
    return {}
