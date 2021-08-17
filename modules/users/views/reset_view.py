from django.shortcuts import render
from django.views import View

from modules.users.forms import ResetPasswordForm


class ResetView(View):
    title = 'Reset Password'

    def get(self, request):
        context = {
            'title': self.title,
            'reset_form': ResetPasswordForm()
        }

        return render(request, 'sites/users/reset.html', context)