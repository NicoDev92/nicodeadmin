from django.shortcuts import render
from inv.models import Producto
import json
from django.db.models import Q
from django.views import View
from django.db import transaction
from .forms import ProductoForm, VentaForm
from .models import Venta, VentaDetalle
from django.http import JsonResponse

from bases.views import SinAutorizacion

class GestionVentaView(SinAutorizacion, View):
    template_name = 'caja.html'
    permission_required = "caja.add_venta"
    def get(self, request):
        producto_form = ProductoForm()
        venta_form = VentaForm()
        return render(request, self.template_name, {'producto_form': producto_form, 'venta_form': venta_form})

    def post(self, request):
        producto_form = ProductoForm(request.POST)
        venta_form = VentaForm(request.POST)
        cart = request.POST.get('cart', '{}')
        cart = json.loads(cart)

        if 'buscar' in request.POST:
            if producto_form.is_valid():
                query = producto_form.cleaned_data['buscar']
                productos = Producto.objects.filter(
                    Q(descripcion__icontains=query) |
                    Q(codigo_barra__icontains=query) |
                    Q(codigo__icontains=query)
                )
                return render(request, self.template_name, {'producto_form': producto_form, 'venta_form': venta_form, 'productos': productos})
        
        
        elif venta_form.is_valid() and cart:
            with transaction.atomic():
                venta = venta_form.save(commit=False)
                venta.usuario = request.user
                venta.total_venta = sum(item['total'] for item in cart.values())
                venta.save()

                for item in cart.values():
                    try:
                        VentaDetalle.objects.create(
                            venta=venta,
                            producto=item.get('name'),
                            precio_unitario=item.get('price'),
                            cantidad=item.get('quantity'),
                            subtotal=item.get('total')
                        )
                        producto = Producto.objects.get(id=item.get('id'))
                        producto.existencia = producto.existencia - item.get('quantity')
                        producto.save()
                        
                    except Producto.DoesNotExist:
                        # Manejar el caso donde el producto no existe
                        return JsonResponse({'success': False, 'error': 'Producto no encontrado'})
                return JsonResponse({'success': True})  # Respuesta JSON de éxito

        # Formulario de venta inválido o carrito vacío
        errors = {}
        if not venta_form.is_valid():
            errors.update(venta_form.errors)
        if not cart:
            errors['cart'] = 'El carrito está vacío'

        return JsonResponse({'success': False, 'errors': errors}, status=400)