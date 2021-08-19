import json

from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.utils.translation import gettext as _

from modules.users.forms import ForgotForm, ResetPasswordForm
from modules.users.models import PanelUser
from zobin.settings import DEFAULT_FROM_EMAIL


class ActivateView(View):
    activation_token = PasswordResetTokenGenerator()
    title = 'Aktywuj konto'

    def get(self, request, uidb64, token):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main_dashboard_view'))

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = PanelUser.objects.get(pk=uid)

        if self.activation_token.check_token(user,token):
            context = {
                'title': self.title,
                'uid': uidb64,
                'token': self.activation_token.make_token(user),
                'form_pass': ResetPasswordForm(user)
            }
            return render(request, 'sites/users/activate.html', context)
        else:
            messages.error(request, json.dumps(
                {
                    'body': _("Link do aktywacji konta wygasł. Skontaktuj sie ze wsparciem klienta, aby zmienić hasło."),
                    'title': _("Nie udało sie aktywować konta!")
                }
            ))
        return HttpResponseRedirect(reverse_lazy("main_dashboard_view"))

    def post(self,request,uidb64,token):
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

        if self.activation_token.check_token(user, token):
            if reset_form.is_valid():
                reset_form.save()
                user.is_active = True
                user.save()
                messages.info(request, json.dumps(
                    {
                        'body': _("Twoje konto zostało aktywowane oraz hasło ustawiono pomyślnie"),
                        'title': _("Konto aktywowane!")
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
                return render(request, "sites/users/activate.html", context)
        else:
            messages.error(request, json.dumps(
                {
                    'body': _("Link do aktywacji konta wygasł. Skontaktuj sie ze wsparciem klienta, aby zmienić hasło."),
                    'title': _("Nie udało sie aktywować konta!")
                }
            ))
            return HttpResponseRedirect(reverse_lazy("main_dashboard_view"))

