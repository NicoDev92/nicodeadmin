from django.urls import path
from .views import EgresosView, IngresosView, IngresoDiarioView, EgresosIngresosAnualesView, \
    generar_pdf_egresos_mensual, generar_pdf_ingresos_mensual, generar_pdf_venta_dia, generar_pdf_factura


urlpatterns = [
    path('reportes/',EgresosIngresosAnualesView.as_view(), name="ingresos_egresos_mensuales"),
    path('reportes/egresos',EgresosView.as_view(), name="egresos_mensuales"),
    path('reportes/ingresos',IngresosView.as_view(), name="ingresos_mensuales"),
    path('reportes/ingresos_diarios',IngresoDiarioView.as_view(), name="ingreso_diario"),
    
    # Descargar pdf's
    
    path('reportes/pdf-gastos/', generar_pdf_egresos_mensual, name="generar_pdf_egresos_mensual"),
    path('reportes/pdf-ventas/', generar_pdf_ingresos_mensual, name="generar_pdf_ventas_mensual"),
    path('reportes/pdf-venta-dia/', generar_pdf_venta_dia, name="generar_pdf_venta_dia"),
    path('reportes/<int:factura_id>/download/', generar_pdf_factura, name='factura_info_download'),
    
]