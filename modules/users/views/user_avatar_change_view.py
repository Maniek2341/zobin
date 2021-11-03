import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from modules.users.models import PanelUser, Rangs


class AvatarChangeView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'zarzad'
    login_url = reverse_lazy('user_login_view')
    title = 'Usuń użytkownika'

    def get(self, request):
        profile = PanelUser.objects.get(pk=request.user.pk)
        context = {
            'title': self.title,
            'profile': profile
        }
        return render(request, 'sites/users/remove.html', context)

    def post(self, request, pk):
        user = PanelUser.objects.get(pk=pk)

        if not user.pk == request.user.pk:
            messages.info(request, json.dumps(
                {
                    'body': "Pomyślnie usunięto użytkownika %s" % user.username,
                    'title': "Usunięto!"
                }
            ))

            user.delete()

        messages.error(request, json.dumps(
            {
                'body': "Nie mozesz usunąć samego siebie.",
                'title': "Błąd!"
            }
        ))
        return HttpResponseRedirect(reverse_lazy("user_list_view"))
