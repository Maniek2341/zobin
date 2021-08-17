from django.urls import path

from modules.main.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name="main_dashboard_view"),
]
