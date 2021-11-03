import json

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from modules.users.forms import LoginForm
from django.utils.translation import gettext as _

from modules.users.models import PanelUser


class LoginView(View):
    title = 'Login Page'

    def get(self, request):
        context = {
            'title': self.title,
            'login_form': LoginForm()
        }

        return render(request, 'sites/users/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember = form.cleaned_data.get("remember")
            user = authenticate(username=username, password=password)
            user1 = PanelUser.objects.get(username=username)

            if user is not None:
                login(request, user)
                if not remember:
                    self.request.session.set_expiry(0)
                    self.request.session.modified = True

                messages.info(request, json.dumps(
                    {
                        'body': _("Pomyślnie zalogowano jako %s") % username,
                        'title': _("Zalogowano!")
                    }
                ))

                return HttpResponseRedirect(reverse_lazy("main_dashboard_view"))
            elif not user1.is_active:
                messages.error(request, json.dumps(
                    {
                        'body': _("Najpierw aktywuj konto!"),
                        'title': _("Brak autoryzacji!")
                    }
                ))
            else:
                messages.error(request, json.dumps(
                    {
                        'body': _("Twój login lub hasło są nieprawidłowe, spróbuj ponownie!"),
                        'title': _("Brak autoryzacji!")
                    }
                ))
        else:
            for header, msg_list in form.errors.as_data().items():
                for error_msg in msg_list:
                    messages.error(request, json.dumps(
                        {
                            'body': str(error_msg.message).capitalize(),
                            'title': _("The current form is not valid")
                        }
                    ))
        context = {
            'title': self.title,
            'login_form': form
        }

        return render(request, "sites/users/login.html", context)