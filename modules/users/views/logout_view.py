import json

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils.translation import gettext as _


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')

    def get(self, request):
        messages.info(request, json.dumps(
            {
                'body': _("You are Successfully logged out, see you later!"),
                'title': _("Successfully logged out!")
            }
        ))

        logout(request)
        return redirect('user_login_view')
