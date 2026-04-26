"""
Ejemplos de uso de decoradores y mixins de autenticación
"""
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from apps.authentication.decorators import role_required
from apps.authentication.mixins import RoleRequiredMixin
from apps.stock.models import Product


# ============================================================================
# EJEMPLOS CON VISTAS FUNCIONALES
# ============================================================================

@role_required('gerente')
def vista_solo_gerente(request):
    """
    Vista accesible solo para usuarios con rol 'gerente'
    """
    return render(request, 'ejemplo.html', {
        'titulo': 'Vista Solo Gerente',
        'mensaje': 'Solo los gerentes pueden ver esto'
    })


@role_required(['gerente', 'administrador'])
def vista_gerente_y_admin(request):
    """
    Vista accesible para gerentes y administradores
    """
    return render(request, 'ejemplo.html', {
        'titulo': 'Vista Gerente y Admin',
        'mensaje': 'Gerentes y administradores pueden ver esto'
    })


@role_required(['gerente', 'administrador', 'empleado'])
def vista_todos_los_roles(request):
    """
    Vista accesible para todos los roles autenticados
    """
    return render(request, 'ejemplo.html', {
        'titulo': 'Vista Todos los Roles',
        'mensaje': 'Todos los usuarios autenticados pueden ver esto'
    })


# ============================================================================
# EJEMPLOS CON VISTAS BASADAS EN CLASE
# ============================================================================

class ProductListViewGerente(RoleRequiredMixin, ListView):
    """
    Lista de productos solo para gerentes
    """
    allowed_roles = ['gerente']
    model = Product
    template_name = 'stock/product_list.html'
    context_object_name = 'products'
    paginate_by = 20


class ProductListViewAdmin(RoleRequiredMixin, ListView):
    """
    Lista de productos para gerentes y administradores
    """
    allowed_roles = ['gerente', 'administrador']
    model = Product
    template_name = 'stock/product_list.html'
    context_object_name = 'products'
    paginate_by = 20


class ProductDetailViewTodos(RoleRequiredMixin, DetailView):
    """
    Detalle de producto para todos los roles
    """
    allowed_roles = ['gerente', 'administrador', 'empleado']
    model = Product
    template_name = 'stock/product_detail.html'
    context_object_name = 'product'


# ============================================================================
# EJEMPLO DE VISTA CON LÓGICA CONDICIONAL POR ROL
# ============================================================================

@role_required(['gerente', 'administrador', 'empleado'])
def dashboard_personalizado(request):
    """
    Dashboard que muestra diferente contenido según el rol
    """
    user = request.user
    context = {
        'user': user,
    }
    
    if user.role == 'gerente':
        # Gerente ve todo
        context['mostrar_reportes'] = True
        context['mostrar_ventas'] = True
        context['mostrar_stock'] = True
        context['puede_editar'] = True
        
    elif user.role == 'administrador':
        # Administrador ve ventas y stock
        context['mostrar_reportes'] = False
        context['mostrar_ventas'] = True
        context['mostrar_stock'] = True
        context['puede_editar'] = True
        
    elif user.role == 'empleado':
        # Empleado solo ve ventas
        context['mostrar_reportes'] = False
        context['mostrar_ventas'] = True
        context['mostrar_stock'] = False
        context['puede_editar'] = False
    
    return render(request, 'dashboard_personalizado.html', context)


# ============================================================================
# EJEMPLO DE MIXIN PERSONALIZADO
# ============================================================================

class GerenteRequiredMixin(RoleRequiredMixin):
    """
    Mixin personalizado que solo permite acceso a gerentes
    """
    allowed_roles = ['gerente']


class AdminRequiredMixin(RoleRequiredMixin):
    """
    Mixin personalizado que permite acceso a gerentes y administradores
    """
    allowed_roles = ['gerente', 'administrador']


# Uso de mixins personalizados
class ReporteVentasView(GerenteRequiredMixin, ListView):
    """
    Reporte de ventas solo para gerentes
    """
    model = Product  # Cambiar por modelo de ventas
    template_name = 'reports/ventas.html'


class GestionProductosView(AdminRequiredMixin, ListView):
    """
    Gestión de productos para gerentes y administradores
    """
    model = Product
    template_name = 'stock/gestion.html'
