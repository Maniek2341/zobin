from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from modules.users.models import Rangs, Dzial, Server, UsersProfile
from .models import PanelUser

class UserProfileInline(admin.StackedInline):
    model = UsersProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]


admin.site.register(PanelUser, UserProfileAdmin)
admin.site.register(Rangs)
admin.site.register(Dzial)
admin.site.register(Server)
