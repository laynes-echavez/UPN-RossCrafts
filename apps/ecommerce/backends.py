"""
Backend de autenticación para clientes de la tienda online
"""
from apps.customers.models import Customer


class CustomerAuthBackend:
    """
    Backend de autenticación personalizado para clientes
    Permite autenticar usando email y contraseña
    """
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Autenticar un cliente usando email y contraseña
        """
        if email is None or password is None:
            return None
        
        try:
            customer = Customer.objects.get(email=email, is_active=True)
            if customer.check_password(password):
                return customer
        except Customer.DoesNotExist:
            return None
        
        return None
    
    def get_user(self, user_id):
        """
        Obtener un cliente por ID
        """
        try:
            return Customer.objects.get(pk=user_id, is_active=True)
        except Customer.DoesNotExist:
            return None
