"""
Middleware de auditoría para registrar acciones de usuarios en el sistema.
Solo audita acciones del dashboard administrativo, no la tienda pública.
"""
from apps.audit.models import AuditLog


class AuditMiddleware:
    """Middleware para registrar acciones de usuarios autenticados en áreas administrativas"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs que NO se auditan (tienda pública y estáticos)
        self.excluded_paths = [
            '/tienda/', 
            '/carrito/', 
            '/cuenta/',
            '/static/', 
            '/media/', 
            '/stripe/webhook/',
            '/checkout/',
            '/payment/',
        ]
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Solo auditar si el usuario es staff (tiene atributo 'role'), no clientes
        if (request.user.is_authenticated and hasattr(request.user, 'role') and
            (request.path.startswith('/dashboard/') or
             request.path.startswith('/stock/') or
             request.path.startswith('/ventas/') or
             request.path.startswith('/clientes/') or
             request.path.startswith('/suppliers/') or
             request.path.startswith('/reports/') or
             request.path.startswith('/auth/usuarios/') or
             request.path.startswith('/admin/'))):
                try:
                    AuditLog.objects.create(
                        user=request.user,
                        action=request.method,
                        url=request.path[:500],
                        ip_address=self.get_client_ip(request),
                        status_code=response.status_code,
                    )
                except Exception as e:
                    # Registrar error en logs pero no interrumpir el flujo
                    import logging
                    logger = logging.getLogger('django')
                    logger.error(f"Error en AuditMiddleware: {e}", exc_info=True)
        
        return response
    
    def get_client_ip(self, request):
        """Obtener la IP real del cliente, considerando proxies"""
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
