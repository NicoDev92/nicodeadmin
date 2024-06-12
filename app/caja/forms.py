from django import forms
from .models import Venta

class ProductoForm(forms.Form):
    buscar = forms.CharField(label='Buscar Producto', widget=forms.TextInput(attrs={'class': 'form-control'}))


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['metodo_pago', 'total_venta', 'fecha_venta'] 
        labels = {'metodo_pago': 'Metodo de pago', 'total_venta': 'Total Venta'}
        widgets = {
            'fecha_venta': forms.DateInput(attrs={'type': 'date'}), 
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control w-100 my-2'
            })
        self.fields['metodo_pago'].widget.choices = self.instance.METODO_PAGO_CHOICES
