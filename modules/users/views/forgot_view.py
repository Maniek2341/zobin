import json

from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.utils.translation import gettext as _

from modules.users.forms import ForgotForm
from modules.users.models import PanelUser
from zobin.settings import DEFAULT_FROM_EMAIL


class ForgotView(View):
    reset_token = PasswordResetTokenGenerator()
    title = 'Forgot password'

    def get(self, request):
        context = {
            'title': self.title,
            'forgot_form': ForgotForm()
        }
        return render(request, 'sites/users/forgot.html', context)

    def post(self, request):
        forgot_form = ForgotForm(request.POST)
        context = {
            'title': self.title,
            'forgot_form': forgot_form
        }

        if forgot_form.is_valid():
            email = forgot_form.cleaned_data["email"]
            qs = PanelUser.objects.filter(email=email)
            mail_subject = _("Wiadomość do zmiany hasła")
            from_email = DEFAULT_FROM_EMAIL
            site = get_current_site(request)
            if qs.exists():
                for user in qs:
                    if user.is_active:
                        mail_content = {
                            'user': user,
                            'email': email,
                            'domain': site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': self.reset_token.make_token(user)
                        }
                        message = render_to_string('sites/mail/forgot_password_confirmation.html', mail_content)
                        if (send_mail(
                                subject=mail_subject,
                                message='',
                                from_email=from_email,
                                recipient_list=[email],
                                fail_silently=True,
                                html_message=message
                        ) == 1):
                            messages.info(request, json.dumps(
                                {
                                    'body': _("Email zmieniający hasło został wysłany, sprawdz skrzynkę pocztową"),
                                    'title': _("Email wysłany!")
                                }
                            ))
                            return HttpResponseRedirect(reverse_lazy("user_login_view"))
                    else:
                        messages.error(request, json.dumps(
                            {
                                'body': _("Twoje konto jest nieaktywne! Aktywuj swoje konto i spróbuj ponownie!"),
                                'title': _("Najpierw aktywuj konto!")
                            }
                        ))
        else:
            messages.warning(request, json.dumps(
                {
                    'body': _("Nie możemy znalezć konta należacego do tego adresu e-mail!"),
                    'title': _("Nie znaleziono konta!")
                }
            ))
        return render(request, "sites/users/forgot.html", context)
