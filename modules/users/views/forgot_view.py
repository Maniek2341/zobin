from django.shortcuts import render
from django.views import View

from modules.users.forms import ForgotForm


class ForgotView(View):
    title = 'Forgot password'

    def get(self, request):
        context = {
            'title': self.title,
            'forgot_form': ForgotForm()
        }
        return render(request, 'sites/users/forgot.html', context)

    def post(self, request):
        pass