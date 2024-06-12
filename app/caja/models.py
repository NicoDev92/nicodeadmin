# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(default=datetime.now)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
    ]
    metodo_pago = models.CharField(max_length=50, null=True, blank=True, choices=METODO_PAGO_CHOICES, default='efectivo')

    def __str__(self):
        return f'Venta {self.id} - Usuario: {self.usuario.username} - Total: {self.total_venta}'

class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.FloatField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle de Venta {self.venta_id} - Producto: {self.producto} - Subtotal: {self.subtotal}'
