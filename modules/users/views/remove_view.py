import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from modules.users.models import UsersProfile, PanelUser


class UserRemoveView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')
    title = 'Usuń użytkownika'

    def get(self, request, pk):
        profile = UsersProfile.objects.get(pk=pk)
        context = {
            'title': self.title,
            'profile': profile
        }
        return render(request, 'sites/users/remove.html', context)

    def post(self, request, pk):
        user = PanelUser.objects.get(pk=pk)

        messages.info(request, json.dumps(
            {
                'body': "Pomyślnie usunięto użytkownika %s" % user.username,
                'title': "Usunięto!"
            }
        ))

        user.delete()
        return HttpResponseRedirect(reverse_lazy("user_list_view"))