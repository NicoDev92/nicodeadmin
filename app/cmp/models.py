from django.db import models

from bases.models import ClaseModelo

# Create your models here.

class Proveedor(ClaseModelo):
    descripcion=models.CharField(
        max_length=100,
        unique=True
        )
    direccion=models.CharField(
        max_length=250,
        null=True, blank=True
        )
    cuil=models.CharField(
        max_length=250,
        null=True, blank=True
        )
    telefono=models.CharField(
        max_length=10,
        null=True, blank=True
    )
    email=models.CharField(
        max_length=250,
        null=True, blank=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = "Proveedores"

class PagoParcial(models.Model):
    factura = models.ForeignKey('Factura', on_delete=models.CASCADE, related_name='pagos_parciales')
    fecha_pago = models.DateTimeField(null=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pago Parcial - Fecha: {self.fecha_pago.strftime('%d/%m/%Y')} - Monto: {self.monto}"

class Factura(ClaseModelo):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_vencimiento = models.DateTimeField(null=False)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    fecha_emision = models.DateTimeField(default=False, null=False)
    es_servicio = models.BooleanField(default=False, null=False)
    es_compra = models.BooleanField(default=False, null=False)
    notas = models.TextField(blank=True, null=True)
    numero_orden_compra = models.CharField(max_length=20, blank=True, null=True)
    total_pagar = models.FloatField(null=False, blank=False)
    numero_factura = models.CharField(
        max_length=20,
        null=False, blank=False
    )
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferecia', 'Transferencia'),
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
    ]
    metodo_pago = models.CharField(max_length=50, null=True, blank=True, choices=METODO_PAGO_CHOICES, default='efectivo')

    ESTADO_FACTURA_CHOICES = [
    ('pendiente', 'Pendiente de Pago'),
    ('pagada', 'Pagada'),
    ('vencida', 'Vencida'),
    ]
    estado_factura = models.CharField(max_length=20, choices=ESTADO_FACTURA_CHOICES, default='pendiente')
    
    def __str__(self):
        return (
            f"Factura {self.numero_factura} - Proveedor: {self.proveedor} - \n"
            f"Total a Pagar: {self.total_pagar} - Estado: {self.get_estado_factura_display()} - \n"
            f"Estado Activo: {'Sí' if self.estado else 'No'} - \n"
            f"Creada el: {self.fecha_creacion} - \n"
            f"Modificada el: {self.fecha_modificacion} - \n"
            f"Creada por: {self.usuario_creador} - \n"
            f"Última modificación por: {self.usuario_modifica}"
        )

    def save(self):
        super(Factura, self).save()

    class Meta:
        verbose_name_plural = "Facturas"
