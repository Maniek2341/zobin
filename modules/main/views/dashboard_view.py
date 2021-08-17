from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from modules.users.models import UsersProfile


class DashboardView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')

    def get(self, request):
        context = {
            'title': 'Dashboard',
            'profile': UsersProfile(),
        }
        return render(request, 'sites/main/dashboard.html', context)
