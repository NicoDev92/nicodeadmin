from django import forms

from .models import Proveedor, Factura, PagoParcial

class ProveedorForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)
    
    class Meta:
        model = Proveedor
        fields = [
            'descripcion', 'direccion', 'cuil',
            'telefono', 'email', 'estado'
        ]
        labels = {'descripcion': "Descripcion", 'direccion':"Dirección", 'cuil':"CUIL/CUIT",
            'telefono':"Teléfono", 'email':"E-mail", 'estado':"Estado" }
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class FacturaForm(forms.ModelForm):
    
    class Meta:
        model = Factura
        fields = [
            'proveedor', 'fecha_vencimiento', 'fecha_pago', 'fecha_emision',
            'es_servicio', 'es_compra', 'notas', 'numero_orden_compra', 'total_pagar', 
            'numero_factura', 'metodo_pago', 'estado_factura'
        ]
        labels = {
            'proveedor': "Proveedor", 
            'fecha_vencimiento': "Fecha de Vencimiento",
            'fecha_pago': "Fecha de Pago", 
            'fecha_emision': "Fecha de Emisión",
            'es_servicio': "Es Servicio", 
            'es_compra': "Es Compra",
            'numero_orden_compra': "Número de Orden de Compra", 
            'total_pagar': "Total a Pagar",
            'numero_factura': "Número de Factura", 
            'metodo_pago': "Método de Pago",
            'estado_factura': "Estado de la Factura"
        }
        widgets = {
            'fecha_vencimiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_pago': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_emision': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notas': forms.Textarea(attrs={'rows': 3}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'estado_factura': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['proveedor'].empty_label = "Seleccione proveedor"

        self.fields['metodo_pago'].widget.choices = self.instance.METODO_PAGO_CHOICES
        self.fields['estado_factura'].widget.choices = self.instance.ESTADO_FACTURA_CHOICES

class PagoParcialForm(forms.ModelForm):
    class Meta:
        model = PagoParcial
        fields = ['factura', 'fecha_pago', 'monto']
        labels = {
            'factura': "Factura", 
            'fecha_pago': "Fecha de Pago", 
            'monto': "Monto"
        }

    def __init__(self, *args, **kwargs):
        factura_id = kwargs.pop('factura_id', None)
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['factura'].widget = forms.HiddenInput()
        elif factura_id:
            self.fields['factura'].initial = Factura.objects.get(pk=factura_id)
            self.fields['factura'].widget = forms.HiddenInput()

