from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from modules.users.models import PanelUser


class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')
    title = 'Profil prywatny'

    def get(self, request):
        profile = PanelUser.objects.get(user=request.user)
        context = {
            'title': self.title,
            'profile': profile
        }
        return render(request, 'sites/users/profile.html', context)

    def post(self, request):
        pass