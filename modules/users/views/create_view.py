import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

from modules.users.forms import CreateUserForm, CreateProfileForm

from django.utils.translation import gettext as _

from modules.users.models import UsersProfile
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
            'profile_form': CreateProfileForm()
        }
        return render(request, 'sites/users/create.html', context)

    def post(self, request):
        site = get_current_site(request)

        user_form = CreateUserForm(request.POST)
        profile_form = CreateProfileForm(request.POST)

        context = {
            'title': self.title,
            "user_form": user_form,
            "profile_form": profile_form
        }

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

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
            for header, msg_list in profile_form.errors.as_data().items():
                for error_msg in msg_list:
                    messages.error(request, json.dumps(
                        {
                            'body': str(error_msg.message).capitalize(),
                            'title': _("The current form is not valid")
                        }
                    ))

        return render(request, "sites/users/create.html", context)