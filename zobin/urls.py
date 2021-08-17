"""zobin URL Configuration

The `urlpatterns` list routes URLs to modules. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function modules
    1. Add an import:  from my_app import modules
    2. Add a URL to urlpatterns:  path('', modules.home, name='home')
Class-based modules
    1. Add an import:  from other_app.modules import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include


def page_not_found_view(request, exception):
    return render(request, 'sites/base/notFound.html', status=404)


def page_not_permission_view(request, exception):
    return render(request, 'sites/base/noPermissions.html', status=403)


urlpatterns = [
    path('user/', include('modules.users.urls')),
    path('', include('modules.main.urls')),
    path('admin/', admin.site.urls),
]


handler404 = page_not_found_view
handler403 = page_not_permission_view


print("WEBSITE URLS loaded...\n\n")