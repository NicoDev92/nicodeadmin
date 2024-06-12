from django.urls import path

from .views import ProveedorView,ProveedorNew, ProveedorEdit, proveedor_inactivar, \
                    FacturaView,FacturaNew, FacturaEdit, \
                    PagoParcialNew, PagoParcialEdit

urlpatterns = [
    # Proveedores
    path('proveedores/',ProveedorView.as_view(), name="proveedor_list"),
    path('proveedores/new',ProveedorNew.as_view(), name="proveedor_new"),
    path('proveedores/edit/<int:pk>',ProveedorEdit.as_view(), name="proveedor_edit"),
    path('proveedores/inactivar/<int:id>',proveedor_inactivar, name="producto_inactivar"),
    
    #Facturas
    path('facturas/',FacturaView.as_view(), name="factura_list"),
    path('facturas/new',FacturaNew.as_view(), name="factura_new"),
    path('facturas/edit/<int:pk>',FacturaEdit.as_view(), name="factura_edit"),
    
    #Pago parcial
    path('pago_parcial/new/<int:id>',PagoParcialNew.as_view(), name="pagoparcial_new"),
    path('pagoparcial/<int:id>/edit/', PagoParcialEdit.as_view(), name='pagoparcial_edit'),

]