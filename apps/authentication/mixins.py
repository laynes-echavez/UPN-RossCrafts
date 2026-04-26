"""
Mixins para vistas basadas en clase con control de acceso por roles
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages


class RoleRequiredMixin(LoginRequiredMixin):
    """
    Mixin que verifica si el usuario tiene uno de los roles permitidos.
    
    Uso:
        class MyView(RoleRequiredMixin, View):
            allowed_roles = ['gerente', 'administrador']
    """
    allowed_roles = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # Verificar que el usuario sea un empleado (User model) y no un cliente (Customer)
        if not hasattr(request.user, 'role'):
            messages.error(request, 'Esta área es solo para empleados del sistema.')
            return redirect('ecommerce:catalog')
        
        if request.user.role not in self.allowed_roles:
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('authentication:access_denied')
        
        return super().dispatch(request, *args, **kwargs)
