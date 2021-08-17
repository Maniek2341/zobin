import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.users.forms import CreateUserForm, UserEditForm, ProfileEditForm
from modules.users.models import PanelUser, UsersProfile

from django.utils.translation import gettext as _

from modules.users.serializers import ProfileSerializer


class UserEditView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')
    title = 'Edytuj użytkownika'

    def get(self, request, pk):
        profile = UsersProfile.objects.get(pk=pk)
        user1 = PanelUser.objects.get(pk=pk)

        profile_form = ProfileEditForm(instance=profile)
        user_form = UserEditForm(instance=user1)

        context = {
            'title': self.title,
            'edit_form': profile_form,
            'user_form': user_form,
            'user1': user1
        }

        return render(request, 'sites/users/edit.html', context)

    def post(self, request, pk):
        profile = UsersProfile.objects.get(pk=pk)
        user1 = PanelUser.objects.get(pk=pk)

        profile_form = ProfileEditForm(request.POST, instance=profile)
        user_form = UserEditForm(request.POST, instance=user1)

        context = {
            'title': self.title,
            'edit_form': profile_form,
            'user_form': user_form,
            'user1': user1
        }

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.info(request, json.dumps(
                {
                    'body': _("Pomyślnie zaaktualizowaleś profil %s") % user1.username,
                    'title': _("Zaktualizowano poprawnie!")
                }
            ))
            return HttpResponseRedirect(reverse_lazy("user_list_view"))
        else:
            for header, msg_list in user_form.errors.as_data().items():
                for error_msg in msg_list:
                    messages.error(request, json.dumps(
                        {
                            'body': str(error_msg.message).capitalize(),
                            'title': _("The current form is valid")
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

        return render(request, 'sites/users/edit.html', context)