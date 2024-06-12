
from .models import Factura
from django.utils import timezone
from datetime import timedelta

def facturas_alertas(request):
    if request.user.is_authenticated:
        now = timezone.now()
        fifteen_days_later = now + timedelta(days=15)
        facturas_vencidas = Factura.objects.filter(
            fecha_vencimiento__lt=timezone.now().date()
        ).exclude(estado_factura='pagada')
        
        facturas_por_vencer = Factura.objects.filter(
            fecha_vencimiento__gte=now.date(),
            fecha_vencimiento__lt=fifteen_days_later.date()
        ).exclude(estado_factura='pagada')
        
        return {
            'facturas_vencidas': facturas_vencidas,
            'facturas_por_vencer': facturas_por_vencer,
        }
    else:
        return {}
