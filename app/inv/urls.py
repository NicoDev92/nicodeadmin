from django.urls import path

from .views import CategoriaView, CategoriaNew, categoria_inactivar, \
    CategoriaEdit, CategoriaDel, SubCategoriaView, \
    SubCategoriaNew, SubCategoriaEdit, SubCategoriaDel, subcategoria_inactivar, \
    MarcaView, MarcaEdit, MarcaNew, marca_inactivar, \
    UMView, UMEdit, UMNew, um_inactivar, \
    ProductoView, ProductoNew, ProductoEdit, producto_inactivar, ExcelUploadView, \
    PrecioNew


urlpatterns = [
    ##Categorias
    path('categorias/', CategoriaView.as_view(), name='categoria_list'),
    path('categorias/new', CategoriaNew.as_view(), name='categoria_new'),
    path('categorias/edit/<int:pk>', CategoriaEdit.as_view(), name='categoria_edit'),
    path('categorias/inactivar/<int:id>', categoria_inactivar, name='categoria_inactivar'),
    path('categorias/delete/<int:pk>', CategoriaDel.as_view(), name='categoria_del'),
    
    ## Subcategorias
    path('subcategorias/', SubCategoriaView.as_view(), name='subcategoria_list'),
    path('subcategorias/new', SubCategoriaNew.as_view(), name='subcategoria_new'),
    path('subcategorias/edit/<int:pk>', SubCategoriaEdit.as_view(), name='subcategoria_edit'),
    path('subcategorias/inactivar/<int:id>', subcategoria_inactivar, name='subcategoria_inactivar'),
    path('subcategorias/delete/<int:pk>', SubCategoriaDel.as_view(), name='subcategoria_del'),
    
    ## Marcas
    path('marcas/',MarcaView.as_view(), name="marca_list"),
    path('marcas/new',MarcaNew.as_view(), name="marca_new"),
    path('marcas/edit/<int:pk>',MarcaEdit.as_view(), name="marca_edit"),
    path('marcas/inactivar/<int:id>',marca_inactivar, name="marca_inactivar"),
    
    ## Unidad medida
    path('um/',UMView.as_view(), name="um_list"),
    path('um/new',UMNew.as_view(), name="um_new"),
    path('um/edit/<int:pk>',UMEdit.as_view(), name="um_edit"),
    path('um/inactivar/<int:id>',um_inactivar, name="um_inactivar"),
    
    ## Productos
    path('productos/',ProductoView.as_view(), name="producto_list"),
    path('productos/new',ProductoNew.as_view(), name="producto_new"),
    path('productos/edit/<int:pk>',ProductoEdit.as_view(), name="producto_edit"),
    path('productos/inactivar/<int:id>',producto_inactivar, name="producto_inactivar"),
    path('productos/cargar-excel/', ExcelUploadView.as_view(), name='excel_upload'),
    
    ## Precios
    path('precio/new/<int:id>',PrecioNew.as_view(), name="precio_new"),

]