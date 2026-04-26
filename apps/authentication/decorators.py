"""
Decoradores personalizados para control de acceso por roles
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """
    Decorador que verifica si el usuario tiene uno de los roles permitidos.
    
    Uso:
        @role_required('gerente')
        @role_required(['gerente', 'administrador'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login')
            
            # Verificar que el usuario sea un empleado (User model) y no un cliente (Customer)
            if not hasattr(request.user, 'role'):
                messages.error(request, 'Esta área es solo para empleados del sistema.')
                return redirect('ecommerce:catalog')
            
            # Convertir a lista si es un string
            roles = [allowed_roles] if isinstance(allowed_roles, str) else allowed_roles
            
            if request.user.role not in roles:
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                return redirect('authentication:access_denied')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
