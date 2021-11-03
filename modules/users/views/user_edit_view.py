import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from modules.users.forms import ProfileEditForm, RangForm
from modules.users.models import PanelUser, Rangs

from django.utils.translation import gettext as _


class UserEditView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'zarzad'
    login_url = reverse_lazy('user_login_view')
    title = 'Edytuj użytkownika'

    def get(self, request, pk):
        profile = PanelUser.objects.get(pk=pk)
        profile_form = ProfileEditForm(instance=profile)

        context = {
            'title': self.title,
            'edit_form': profile_form,
            'user1': profile
        }

        return render(request, 'sites/users/edit.html', context)

    def post(self, request, pk):
        profile = PanelUser.objects.get(pk=pk)

        profile_form = ProfileEditForm(request.POST, instance=profile)

        context = {
            'title': self.title,
            'edit_form': profile_form,
            'user1': profile
        }

        if profile_form.is_valid():
            profile_form.save()
            messages.info(request, json.dumps(
                {
                    'body': _("Pomyślnie zaaktualizowaleś profil %s") % profile.username,
                    'title': _("Zaktualizowano poprawnie!")
                }
            ))
            return HttpResponseRedirect(reverse_lazy("user_list_view"))
        else:
            for header, msg_list in profile_form.errors.as_data().items():
                for error_msg in msg_list:
                    messages.error(request, json.dumps(
                        {
                            'body': str(error_msg.message).capitalize(),
                            'title': _("The current form is not valid")
                        }
                    ))

        return render(request, 'sites/users/edit.html', context)


class RangEditView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'zarzad'
    login_url = reverse_lazy('user_login_view')
    title = 'Edytuj Rangę'

    def get(self, request, pk):
        rangs = Rangs.objects.get(pk=pk)

        rang_form = RangForm(instance=rangs)

        context = {
            'title': self.title,
            'rang_form': rang_form,
            'rang': rangs,
        }

        return render(request, 'sites/rangs/edit.html', context)

    def post(self, request, pk):
        rangs = Rangs.objects.get(pk=pk)

        rang_form = RangForm(request.POST, instance=rangs)

        context = {
            'title': self.title,
            'rang_form': rang_form,
            'rang': rangs,
        }

        if rang_form.is_valid():
            rang_form.save()
            messages.info(request, json.dumps(
                {
                    'body': _("Pomyślnie zaaktualizowaleś rangę %s") % rangs.ranga,
                    'title': _("Zaktualizowano poprawnie!")
                }
            ))
            return HttpResponseRedirect(reverse_lazy("rang_list_view"))
        else:
            for header, msg_list in rang_form.errors.as_data().items():
                for error_msg in msg_list:
                    messages.error(request, json.dumps(
                        {
                            'body': str(error_msg.message).capitalize(),
                            'title': _("The current form is valid")
                        }
                    ))

        return render(request, 'sites/rangs/edit.html', context)