from django.urls import path
from .views import GestionVentaView

urlpatterns = [
    path('punto_venta/', GestionVentaView.as_view(), name='punto_venta'),
]
