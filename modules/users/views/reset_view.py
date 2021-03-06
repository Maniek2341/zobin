import json

from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.utils.translation import gettext as _

from modules.users.forms import ResetPasswordForm
from modules.users.models import PanelUser


class ResetView(View):
    title = 'Resetuj hasło'
    reset_token = PasswordResetTokenGenerator()

    def get(self, request, uidb64, token):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main_dashboard_view'))

        context = {}
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = PanelUser.objects.get(pk=uid)
        if self.reset_token.check_token(user, token):

            context = {
                'title': self.title,
                'reset_form': ResetPasswordForm(user),
                'uid': uidb64,
                'token': token
            }
            return render(request, 'sites/users/reset.html', context)
        else:
            messages.error(request, json.dumps(
                {
                    'body': _("Link do zmiany hasła wygasł. Skontaktuj sie ze wsparciem klienta, aby zmienić hasło."),
                    'title': _("Nie udało sie zmienić hasła!")
                }
            ))
            return HttpResponseRedirect(reverse_lazy("main_dashboard_view"))

    def post(self,request, uidb64, token):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main_dashboard_view'))

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = PanelUser.objects.get(pk=uid)
        reset_form = ResetPasswordForm(data=request.POST, user=user)

        context = {
            'title': self.title,
            'reset_form': reset_form,
            'uid': uidb64,
            'token': token
        }

        if self.reset_token.check_token(user, token):
            if reset_form.is_valid():
                reset_form.save()
                messages.info(request, json.dumps(
                    {
                        'body': _("Twoje hasło zostało pomyślnie zmienione. Teraz mozesz się zalogować używając "
                                  "nowego hasła."),
                        'title': _("Hasło zmienione!")
                    }
                ))
                return HttpResponseRedirect(reverse_lazy("user_login_view"))
            else:
                for header, msg_list in reset_form.errors.as_data().items():
                    for error_msg in msg_list:
                        messages.error(request, json.dumps(
                            {
                                'body': str(error_msg.message).capitalize(),
                                'title': _("The current form is not valid")
                            }
                        ))
                return render(request, "sites/users/forgot.html", context)
        else:
            messages.error(request, json.dumps(
                {
                    'body': _("Link do zmiany hasła wygasł. Skontaktuj sie ze wsparciem klienta, aby zmienić hasło."),
                    'title': _("Nie udało sie zmienić hasła!")
                }
            ))
            return HttpResponseRedirect(reverse_lazy("main_dashboard_view"))