from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from modules.users.forms import ProfileForm
from modules.users.models import PanelUser


class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_login_view')
    title = 'Profil prywatny'

    def get(self, request):
        profile = PanelUser.objects.get(id=request.user.id)
        form = ProfileForm(instance=profile)
        context = {
            'title': self.title,
            'profile': profile,
            'form': form
        }
        return render(request, 'sites/users/profile.html', context)

    def post(self, request):
        pass