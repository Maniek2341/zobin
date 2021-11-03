from django.urls import path

from modules.wnioski.views import PropozycjaView, SkargaView, UrlopView, PochwalaView, WypowiedzenieView

urlpatterns = [
    path('propozycja/', PropozycjaView.as_view(), name="wniosek_propozycja_view"),
    path('skarga/', SkargaView.as_view(), name="wniosek_skarga_view"),
    path('urlop/', UrlopView.as_view(), name="wniosek_urlop_view"),
    path('pochwala/', PochwalaView.as_view(), name="wniosek_pochwala_view"),
    path('wypowiedzenie/', WypowiedzenieView.as_view(), name="wniosek_wypowiedzenie_view"),
]
