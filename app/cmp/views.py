from decimal import Decimal, ROUND_HALF_UP
import os
import datetime

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy


from cmp.forms import ProveedorForm, FacturaForm, PagoParcialForm
from cmp.models import Proveedor, Factura, PagoParcial
from bases.views import SinAutorizacion

class ProveedorView(LoginRequiredMixin,SinAutorizacion, generic.ListView):
    model = Proveedor
    permission_required = "cmp.view_proveedor"
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'
    
    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener el usuario de modificación para cada producto
        for proveedor in queryset:
            if proveedor.usuario_modifica:
                usuario_modifica = User.objects.filter(pk=proveedor.usuario_modifica).first()
                proveedor.usuario_modifica_nombre = usuario_modifica.username if usuario_modifica else None

        return queryset

class ProveedorNew(LoginRequiredMixin,SinAutorizacion, generic.CreateView):
    model=Proveedor
    permission_required = "cmp.add_proveedor"
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Nuevo"

    def form_valid(self, form):
        form.instance.usuario_creador = self.request.user
        redirect_url = reverse_lazy("cmp:proveedor_list")
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('descripcion', 'La descripción ya existe. Por favor, ingrese una descripción diferente.')
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return super().form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)

class ProveedorEdit(LoginRequiredMixin,SinAutorizacion, generic.UpdateView):
    model=Proveedor
    permission_required = "cmp.change_proveedor"
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Nuevo"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        redirect_url = reverse_lazy("cmp:proveedor_list")
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('descripcion', 'La descripción ya existe. Por favor, ingrese una descripción diferente.')
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return super().form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)

def proveedor_inactivar(request, id):
    proveedor = Proveedor.objects.filter(pk=id).first()
    contexto = {}
    template_name = "cmp/catalogos_del.html"
    
    if not proveedor:
        return redirect("cmp:proveedor_list")
    
    if request.method == "GET":
        contexto = {'obj': proveedor}
    
    if request.method == 'POST':
        # Alternar entre activo e inactivo
        proveedor.usuario_modifica = request.user.id
        proveedor.estado = not proveedor.estado
        proveedor.save()
        return redirect("cmp:proveedor_list")

class FacturaView(LoginRequiredMixin,SinAutorizacion, generic.ListView):
    model = Factura
    permission_required = "cmp.view_factura"
    template_name = "cmp/factura_list.html"
    context_object_name = "obj"
    login_url='bases:login'
    
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('pagos_parciales')

        # Obtener el usuario de modificación para cada producto
        for factura in queryset:
            if factura.usuario_modifica:
                usuario_modifica = User.objects.filter(pk=factura.usuario_modifica).first()
                factura.usuario_modifica_nombre = usuario_modifica.username if usuario_modifica else None

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calcular la suma de los montos de los pagos parciales para cada factura
        for factura in context['obj']:
            factura.suma_pagos_parciales = factura.pagos_parciales.aggregate(Sum('monto'))['monto__sum'] or Decimal('0')
            remanente_pago = Decimal(factura.total_pagar) - factura.suma_pagos_parciales
            factura.remanente_pago = remanente_pago.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return context

class FacturaNew(LoginRequiredMixin,SinAutorizacion, generic.CreateView):
    model=Factura
    permission_required = "cmp.add_factura"
    form_class=FacturaForm
    template_name="cmp/factura_form.html"
    context_object_name = 'obj'
    success_url= reverse_lazy("cmp:factura_list")
    success_message="Factura Nueva"

    def form_valid(self, form):
        form.instance.usuario_creador = self.request.user
        redirect_url = reverse_lazy("cmp:factura_list")
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('descripcion', 'La descripción ya existe. Por favor, ingrese una descripción diferente.')
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return super().form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)

class FacturaEdit(LoginRequiredMixin,SinAutorizacion, generic.UpdateView):
    model=Factura
    permission_required = "cmp.change_factura"
    form_class=FacturaForm
    template_name="cmp/factura_form.html"
    context_object_name = 'obj'
    success_url= reverse_lazy("cmp:factura_list")
    success_message="Factura Nueva"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        redirect_url = reverse_lazy("cmp:factura_list")
        try:
            response = super().form_valid(form)
            
            factura = Factura.objects.get(id=self.kwargs['pk'])
            monto_total_pagos_parciales = PagoParcial.objects.filter(factura=factura).aggregate(Sum('monto'))['monto__sum'] or Decimal('0')

            if monto_total_pagos_parciales >= Decimal(factura.total_pagar):
                form.instance.fecha_pago = form.instance.fecha_pago
                form.instance.estado_factura = 'pagada'
            elif monto_total_pagos_parciales <= Decimal(factura.total_pagar):
                form.instance.estado_factura = 'pendiente'
                
            return super().form_valid(form)
        
        except IntegrityError:
            form.add_error('descripcion', 'La descripción ya existe. Por favor, ingrese una descripción diferente.')
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)

## Pagos Parciales

class PagoParcialNew(LoginRequiredMixin,SinAutorizacion, generic.CreateView):
    model = PagoParcial
    permission_required = "cmp.add_pagoparcial"
    form_class = PagoParcialForm
    template_name = "cmp/pagoparcial_form.html"
    context_object_name = 'obj'
    success_url = reverse_lazy("cmp:factura_list")
    success_message = "Pago parcial Nuevo"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['factura_id'] = self.kwargs['id'] 
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        factura = Factura.objects.get(id=self.kwargs['id'])
        monto_total_pagos_parciales = PagoParcial.objects.filter(factura=factura).aggregate(Sum('monto'))['monto__sum'] or Decimal('0')
        context['monto_total_pagar'] = factura.total_pagar
        context['monto_total_pagado'] = monto_total_pagos_parciales
        return context

    def form_valid(self, form):
        form.instance.usuario_creador = self.request.user
        form.instance.factura_id = self.kwargs['id']  
        redirect_url = reverse_lazy("cmp:factura_list")
        try:
            response = super().form_valid(form)
            factura = Factura.objects.get(id=self.kwargs['id'])
            monto_total_pagos_parciales = PagoParcial.objects.filter(factura=factura).aggregate(Sum('monto'))['monto__sum'] or Decimal('0')
            
            if monto_total_pagos_parciales >= Decimal(factura.total_pagar):
                factura.fecha_pago = form.instance.fecha_pago
                factura.estado_factura = 'pagada'
                factura.save()
            return response
        except IntegrityError:
            form.add_error('descripcion', 'La descripción ya existe. Por favor, ingrese una descripción diferente.')
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return super().form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)

class PagoParcialEdit(LoginRequiredMixin,SinAutorizacion, generic.UpdateView):
    model = PagoParcial
    permission_required = "cmp.change_pagoparcial"
    form_class = PagoParcialForm
    template_name = "cmp/pagoparcial_form.html"
    context_object_name = 'obj'
    success_url = reverse_lazy("cmp:factura_list")
    success_message = "Pago parcial editado"

    def get_object(self, queryset=None):
        pago_id = self.request.GET.get('pago_id')
        return get_object_or_404(PagoParcial, id=pago_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        factura = Factura.objects.get(id=self.kwargs['id'])
        monto_total_pagos_parciales = PagoParcial.objects.filter(factura=factura).aggregate(Sum('monto'))['monto__sum'] or Decimal('0')
        context['monto_total_pagar'] = factura.total_pagar
        context['monto_total_pagado'] = monto_total_pagos_parciales
        
        return context

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        form.instance.factura_id = self.kwargs['id']
        redirect_url = reverse_lazy("cmp:factura_list")
        try:
            response = super().form_valid(form)
            factura = Factura.objects.get(id=self.kwargs['id'])
            monto_total_pagos_parciales = PagoParcial.objects.filter(factura=factura).aggregate(Sum('monto'))['monto__sum'] or Decimal('0')

            if monto_total_pagos_parciales >= Decimal(factura.total_pagar):
                factura.fecha_pago = form.instance.fecha_pago
                factura.estado_factura = 'pagada'
                factura.save()
            elif monto_total_pagos_parciales <= Decimal(factura.total_pagar):
                factura.estado_factura = 'pendiente'
                factura.save()
                

            return response
        except IntegrityError:
            form.add_error('descripcion', 'La descripción ya existe. Por favor, ingrese una descripción diferente.')
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return super().form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)

