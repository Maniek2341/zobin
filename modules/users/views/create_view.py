import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from modules.users.forms import CreateUserForm

from django.utils.translation import gettext as _

from modules.users.models import UsersProfile


class CreateView(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login_view')
    title = "Create User"

    def get(self, request):
        context = {
            'title': self.title.title,
            'user_form': CreateUserForm()
        }
        return render(request, 'sites/users/create.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            if user.dzial == 'Zarzad':
                content_type = ContentType.objects.get_for_model(UsersProfile)
                permission = Permission.objects.create(
                    codename='zarzad',
                    name='Zarzadza serwerem',
                    content_type=content_type
                )


            user.save()

            messages.success(request, json.dumps(
                {
                    'body': _("Thanks for your registration. A confirmation link has been sent to your email"),
                    'title': _("Account registered!")
                }
            ))
            return HttpResponseRedirect(reverse_lazy("user_create_view"))
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
                "user_form": CreateUserForm(),
            }
            return render(request, "sites/users/create.html", context)