from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from modules.main.models import Messages
from modules.users.models import PanelUser


class DashboardView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')

    def get(self, request):
        czlonek = Messages.objects.filter(user__dzial=1).order_by('-created_at')[:5]
        dyrekcja = Messages.objects.filter(user__dzial=2).order_by('-created_at')[:5]
        zarzad = Messages.objects.filter(user__dzial=3).order_by('-created_at')[:5]
        users = PanelUser.objects.all()

        context = {
            'title': 'Dashboard',
            'czlonek': czlonek,
            'dyrekcja': dyrekcja,
            'zarzad': zarzad,
            'users': users,
        }
        return render(request, 'sites/main/dashboard.html', context)
