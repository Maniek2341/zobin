import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from modules.users.models import PanelUser, Rangs


class UserRemoveView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'zarzad'
    login_url = reverse_lazy('user_login_view')
    title = 'Usuń użytkownika'

    def get(self, request, pk):
        profile = PanelUser.objects.get(pk=pk)
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

class RangRemoveView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'zarzad'
    login_url = reverse_lazy('user_login_view')
    title = 'Usuń rangę'

    def get(self, request, pk):
        rang = Rangs.objects.get(pk=pk)
        context = {
            'title': self.title,
            'rang': rang
        }
        return render(request, 'sites/rangs/remove.html', context)

    def post(self, request, pk):
        rang = Rangs.objects.get(pk=pk)

        messages.info(request, json.dumps(
            {
                'body': "Pomyślnie usunięto rangę %s" % rang.ranga,
                'title': "Usunięto!"
            }
        ))

        rang.delete()
        return HttpResponseRedirect(reverse_lazy("rang_list_view"))