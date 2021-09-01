import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View

from modules.users.forms import CreateUserForm, RangForm

from django.utils.translation import gettext as _

from modules.users.models import PanelUser
from zobin.settings import DEFAULT_FROM_EMAIL


class CreateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'zarzad'
    login_url = reverse_lazy('user_login_view')
    title = "Create User"
    activation_token = PasswordResetTokenGenerator()

    def get(self, request):
        context = {
            'title': self.title.title,
            'user_form': CreateUserForm(),
        }
        return render(request, 'sites/users/create.html', context)

    def post(self, request):
        site = get_current_site(request)

        user_form = CreateUserForm(request.POST)

        context = {
            'title': self.title,
            "user_form": user_form,
        }

        if user_form.is_valid():
            content_type = ContentType.objects.get_for_model(PanelUser)
            permission = Permission.objects.get(
                codename='zarzad',
                content_type=content_type,
            )
            user = user_form.save()
            if user.dzial == 3:
                user.user_permissions.add(permission)
                user.save()
            user.save()

            mail_content = {
                'user': user,
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': self.activation_token.make_token(user)
            }

            message = render_to_string('sites/mail/account_confirm.html', mail_content)

            send_mail(
                subject=_("Wiadomość potwierdzająca"),
                message=_('Welcome %s,\n\n You get this mail because you do yours first right step, '
                          'you registered a account on %s and we are very happy about it!\n\nYour login '
                          'credentials:\nUsername: %s\n \nMake sure to keep this e-mail secure!\n\nTo '
                          'complete the registration process please verify you account by clicking on this '
                          'link:\nhttp://%s/%s/%s') % (
                            user.first_name, site.domain, user.username, site.domain,
                            mail_content.get('uid', ''),
                            mail_content.get('token', '')
                        ),
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
                html_message=message
            )

            messages.info(request, json.dumps(
                {
                    'body': _("Link aktywacyjny został wysłany do %s" % user.username),
                    'title': _("Konto założone!")
                }
            ))
            return HttpResponseRedirect(reverse_lazy("main_dashboard_view"))
        else:
            for header, msg_list in user_form.errors.as_data().items():
                for error_msg in msg_list:
                    messages.error(request, json.dumps(
                        {
                            'body': str(error_msg.message).capitalize(),
                            'title': _("Błąd!")
                        }
                    ))

        return render(request, "sites/users/create.html", context)


class RangsCreateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'zarzad'
    login_url = reverse_lazy('user_login_view')
    title = "Stwórz range"
    activation_token = PasswordResetTokenGenerator()

    def get(self, request):
        context = {
            'title': self.title.title,
            'rang_form': RangForm(),
        }
        return render(request, 'sites/rangs/create.html', context)

    def post(self, request):

        rang_form = RangForm(request.POST)

        context = {
            'title': self.title,
            "rang_form": rang_form,
        }

        if rang_form.is_valid():
            ranga = rang_form.save()
            ranga.save()

            messages.info(request, json.dumps(
                {
                    'body': _("Pomyślnie stworzono rangę %s." % ranga.ranga),
                    'title': _("Dodano range!")
                }
            ))
            return HttpResponseRedirect(reverse_lazy("main_dashboard_view"))
        else:
            for header, msg_list in rang_form.errors.as_data().items():
                for error_msg in msg_list:
                    messages.error(request, json.dumps(
                        {
                            'body': str(error_msg.message).capitalize(),
                            'title': _("Błąd!")
                        }
                    ))

        return render(request, "sites/rangs/create.html", context)