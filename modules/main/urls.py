from django.urls import path

from modules.main.views import DashboardView, MessageView

urlpatterns = [
    path('', DashboardView.as_view(), name="main_dashboard_view"),
    path('mess/', MessageView.as_view(), name="main_message_view"),
]
