
from .models import Producto

def stock_alerta(request):
    
    if request.user.is_authenticated:
        productos_stock_bajo = Producto.objects.filter(
            existencia__lte= 0
        ).exclude(estado=False)
        
        
        return {
            'productos_stock_bajo' : productos_stock_bajo,
        }
    else:
        return {}
