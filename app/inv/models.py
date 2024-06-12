from django.db import models
from bases.models import ClaseModelo


# Create your models here.

## Categorías
class Categoria(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descriopción de la categoría',
        unique=True 
    )
    
    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper() 
        super(Categoria, self).save()
    
    class Meta:
        verbose_name_plural = "Categorias"

## Subcategorías
class SubCategoria(ClaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100, 
        help_text='Descriopción de la categoría'
    )
    
    def __str__(self):
        return '{}: {}'.format(self.categoria.descripcion, self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper() 
        super(SubCategoria, self).save()
        
    class Meta:
        verbose_name_plural = "Sub Categorias"
        unique_together = ('categoria', 'descripcion')

## Marcas
class Marca(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la categoría',
        unique=True 
    )
    
    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self): 
        super(Marca, self).save()

    class Meta:
        verbose_name_plural = "Marca"

## Unidad de medida
class UnidadMedida(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Unidad Medida',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(UnidadMedida, self).save()

    class Meta:
        verbose_name_plural = "Unidades de Medida"

## Producto
class Producto(ClaseModelo):
    codigo = models.CharField(
        max_length=20,
        unique=True
    )
    codigo_barra = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    existencia = models.IntegerField(default=0)
    ultima_compra = models.DateField(null=True, blank=True)
    precio_venta = models.FloatField(null=True, blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, null=True, blank=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Producto,self).save()
    
    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ('codigo','codigo_barra')

class Precio(ClaseModelo):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    porcentaje_fijo = models.FloatField()
    porcentaje_variable = models.FloatField()
    porcentaje_ganancia = models.FloatField()
    precio_costo = models.FloatField()
    precio_final = models.FloatField()
    
    def save(self):
        super(Precio, self).save()
    
    class Meta:
        verbose_name_plural = "Precios"