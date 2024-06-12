from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def color_class(fecha_vencimiento, estado_factura):
    # Asegurarse de que la fecha de vencimiento sea un objeto date
    if isinstance(fecha_vencimiento, datetime):
        fecha_vencimiento = fecha_vencimiento.date()
    
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()

    # Calcular la diferencia en días entre la fecha de vencimiento y la fecha actual
    diferencia = fecha_vencimiento - fecha_actual

    # Aplicar la clase correspondiente según la diferencia en días
    if estado_factura == 'pagada':
        return 'bg-inactive-own'
    elif diferencia.days < 0 and estado_factura != 'pagada':
        return 'bg-danger-own'  # Si ya está vencido o se pasó el vencimiento, clase roja
    elif diferencia.days <= 15 and estado_factura != 'pagada':
        return 'bg-warning-own'  # Si faltan 15 días o menos para el vencimiento, clase amarilla
    elif diferencia.days >= 15 and estado_factura != 'pagada':
        return 'bg-success-own'  # Si faltan más de 15 días para el vencimiento, clase verde
