from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View


class WypowiedzenieView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')

    def get(self, request):
        context = {
            'title': 'Wypowiedzenie',
        }
        return render(request, 'sites/wnioski/wypowiedzenie.html', context)
