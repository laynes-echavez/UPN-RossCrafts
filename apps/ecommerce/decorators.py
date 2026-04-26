"""
Decoradores para vistas de clientes
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from apps.customers.models import Customer


def customer_login_required(view_func):
    """
    Decorador que verifica si el usuario autenticado es un Customer
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('ecommerce:customer_login')
        
        # Verificar que sea un Customer, no un User de staff
        if not isinstance(request.user, Customer):
            messages.error(request, 'Esta área es solo para clientes de la tienda.')
            return redirect('ecommerce:customer_login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
