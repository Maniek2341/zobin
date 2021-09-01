import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.utils.translation import gettext as _

from modules.main.forms import MessageForm
from modules.main.models import Messages
from modules.users.models import PanelUser


class MessageView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')

    def get(self, request):
        context = {
            'title': 'Dashboard',
            'message_form': MessageForm(),
        }
        return render(request, 'sites/main/message.html', context)

    def post(self, request):
        user = PanelUser.objects.get(username=request.user.username, dzial=request.user.dzial)
        message_form = MessageForm(request.POST)

        context = {
            'title': 'Dashboard',
            'message_form': message_form,
        }

        if message_form.is_valid():
            mess = message_form.save(commit=False)
            mess.user = user
            mess.save()
        else:
            for header, msg_list in message_form.errors.as_data().items():
                for error_msg in msg_list:
                    messages.error(request, json.dumps(
                        {
                            'body': str(error_msg.message).capitalize(),
                            'title': _("The current form is not valid")
                        }
                    ))
            return render(request, "sites/main/message.html", context)

        messages.info(request, json.dumps(
            {
                'body': "Pomyślnie utworzono wiadomosc.",
                'title': "Utworzono!"
            }
        ))
        return HttpResponseRedirect(reverse_lazy("main_message_view"))