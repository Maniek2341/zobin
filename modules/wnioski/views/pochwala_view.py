from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View


class PochwalaView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')

    def get(self, request):
        context = {
            'title': 'Pochwala',
        }
        return render(request, 'sites/wnioski/pochwala.html', context)
