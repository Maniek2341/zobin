import json
import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.users.forms import CreateUserForm

from django.utils.translation import gettext as _

from modules.users.models import PanelUser, Rangs
from rest_framework import viewsets, generics


class ListUserView(PermissionRequiredMixin, LoginRequiredMixin, APIView):
    permission_required = 'zarzad'
    login_url = reverse_lazy('user_login_view')
    title = 'Lista użytkowników'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sites/users/list_users.html'

    def get(self, request):
        queryset = PanelUser.objects.all()
        context = {
            'users': queryset,
            'title': self.title,
        }
        return Response(context)


class ListRangView(PermissionRequiredMixin, LoginRequiredMixin, APIView):
    permission_required = 'zarzad'
    login_url = reverse_lazy('user_login_view')
    title = 'Lista użytkowników'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sites/rangs/list.html'

    def get(self, request):
        context = {
            'rangs': Rangs.objects.all(),
            'title': self.title,
        }
        return Response(context)

