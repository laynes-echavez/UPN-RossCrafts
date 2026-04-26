"""
Context processors para stock
"""
from .models import Product
from django.db.models import F


def low_stock_alert(request):
    """
    Agrega al contexto global la cantidad de productos con stock bajo
    """
    # Solo ejecutar para usuarios staff (con rol), no para clientes de la tienda
    if request.user.is_authenticated and hasattr(request.user, 'role'):
        low_stock_count = Product.objects.filter(
            is_active=True,
            stock_quantity__lte=F('min_stock_quantity')
        ).count()
        
        return {
            'low_stock_count': low_stock_count
        }
    
    return {
        'low_stock_count': 0
    }
