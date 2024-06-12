from django import forms
from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto, Precio

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descripcion', 'estado']
        labels = { "descripcion": "Descripcion de la categoría",
                    "estado": "Estado"}
        widget = {'descripcion': forms.TextInput}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

##Subcategoria form
class SubCategoriaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True)
        .order_by('descripcion')
    )
    class Meta:
        model = SubCategoria
        fields = ['categoria','descripcion', 'estado']
        labels = { "descripcion": "Subcategoria",
                    "estado": "Estado"}
        widget = {'descripcion': forms.TextInput()}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control w-100 my-2'
            })
        self.fields['categoria'].empty_label = "Seleccione categoría"

## Marca form

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['descripcion', 'estado']
        labels = {'descripcion': "Descripción de la Marca", "estado": "Estado"}
        widget = {'descripcion': forms.TextInput()}  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

## Unidad de medida form
class UMForm(forms.ModelForm):
    class Meta:
        model=UnidadMedida
        fields = ['descripcion','estado']
        labels= {'descripcion': "Descripción de la Marca",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

## Productos Form

class ProductoForm(forms.ModelForm):
    subcategoria = forms.ModelChoiceField(
        queryset=SubCategoria.objects.filter(estado=True)
        .order_by('descripcion')
    )
    
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.filter(estado=True)
        .order_by('descripcion')
    )
    
    unidad_medida = forms.ModelChoiceField(
        queryset=UnidadMedida.objects.filter(estado=True)
        .order_by('descripcion')
    )
    
    class Meta:
        model=Producto
        fields=['codigo','codigo_barra','descripcion','estado', \
                'existencia','ultima_compra',
                'marca','subcategoria','unidad_medida']
        exclude = ['usuario_modifica','fecha_modificacion','usuario_creador','fecha_creacion']
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True

## Agregar precio Form

class PrecioForm(forms.ModelForm):
    class Meta:
        model = Precio
        fields = ['producto', 'porcentaje_fijo', 'porcentaje_variable', 
                'porcentaje_ganancia', 'precio_costo', 'precio_final']
        labels = {
            'producto' : 'Producto',
            'porcentaje_fijo' : '% Costo Fijo',
            'porcentaje_variable' : '% Costo Variable', 
            'porcentaje_ganancia' : '% Ganancia', 
            'precio_costo' : 'Precio de costo', 
            'precio_final' : 'Precio Final'
        }
    def __init__(self, *args, **kwargs):
        producto_id = kwargs.pop('producto_id', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        if producto_id:
            self.fields['producto'].initial = producto_id 
            self.fields['producto'].widget = forms.HiddenInput()


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Seleccionar archivo Excel', help_text='Formatos permitidos: .xls, .xlsx')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith(('.xls', '.xlsx')):
                raise forms.ValidationError('Formato de archivo no válido. Solo se permiten archivos .xls o .xlsx.')
        return file

