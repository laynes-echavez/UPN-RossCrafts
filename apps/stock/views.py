from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, F
from apps.authentication.mixins import RoleRequiredMixin
from apps.authentication.decorators import role_required
from .models import Product, Category, StockMovement
from .forms import ProductForm, CategoryForm, StockMovementForm, ImportExcelForm
from .utils import import_products_from_excel


class ProductListView(RoleRequiredMixin, ListView):
    """Lista de productos con filtros y paginación"""
    allowed_roles = ['gerente', 'administrador', 'empleado']
    model = Product
    template_name = 'stock/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.select_related('category').order_by('name')
        
        # Filtro por búsqueda
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(sku__icontains=search)
            )
        
        # Filtro por categoría
        category_id = self.request.GET.get('category', '')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filtro por nivel de stock
        stock_level = self.request.GET.get('stock_level', '')
        if stock_level == 'low':
            queryset = queryset.filter(stock_quantity__lte=F('min_stock_quantity'))
        elif stock_level == 'out':
            queryset = queryset.filter(stock_quantity=0)
        
        # Filtro por estado
        is_active = self.request.GET.get('is_active', '')
        if is_active == '1':
            queryset = queryset.filter(is_active=True)
        elif is_active == '0':
            queryset = queryset.filter(is_active=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('name')
        context['search'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_stock_level'] = self.request.GET.get('stock_level', '')
        context['selected_is_active'] = self.request.GET.get('is_active', '')
        return context


class ProductCreateView(RoleRequiredMixin, CreateView):
    """Crear nuevo producto"""
    allowed_roles = ['gerente', 'administrador']
    model = Product
    form_class = ProductForm
    template_name = 'stock/product_form.html'
    success_url = reverse_lazy('stock:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Producto "{form.instance.name}" creado exitosamente.')
        return super().form_valid(form)


class ProductUpdateView(RoleRequiredMixin, UpdateView):
    """Editar producto existente"""
    allowed_roles = ['gerente', 'administrador']
    model = Product
    form_class = ProductForm
    template_name = 'stock/product_form.html'
    success_url = reverse_lazy('stock:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Producto "{form.instance.name}" actualizado exitosamente.')
        return super().form_valid(form)


class ProductDeleteView(RoleRequiredMixin, DeleteView):
    """Eliminar producto (soft delete)"""
    allowed_roles = ['gerente']
    model = Product
    template_name = 'stock/product_confirm_delete.html'
    success_url = reverse_lazy('stock:product_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Soft delete
        self.object.is_active = False
        self.object.save()
        messages.success(request, f'Producto "{self.object.name}" desactivado exitosamente.')
        return redirect(self.success_url)


class ProductDetailView(RoleRequiredMixin, DetailView):
    """Detalle de producto con historial de movimientos"""
    allowed_roles = ['gerente', 'administrador', 'empleado']
    model = Product
    template_name = 'stock/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Últimos 50 movimientos de stock
        context['movements'] = StockMovement.objects.filter(
            product=self.object
        ).select_related('user').order_by('-created_at')[:50]
        return context


class CategoryListView(RoleRequiredMixin, ListView):
    """Lista de categorías"""
    allowed_roles = ['gerente', 'administrador', 'empleado']
    model = Category
    template_name = 'stock/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.order_by('name')


class StockMovementListView(RoleRequiredMixin, ListView):
    """Historial de movimientos de stock"""
    allowed_roles = ['gerente', 'administrador', 'empleado']
    model = StockMovement
    template_name = 'stock/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = StockMovement.objects.select_related(
            'product', 'user'
        ).order_by('-created_at')
        
        # Filtro por producto
        product_id = self.request.GET.get('product', '')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        # Filtro por tipo de movimiento
        movement_type = self.request.GET.get('movement_type', '')
        if movement_type:
            queryset = queryset.filter(movement_type=movement_type)
        
        # Filtro por rango de fechas
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_active=True).order_by('name')
        context['selected_product'] = self.request.GET.get('product', '')
        context['selected_movement_type'] = self.request.GET.get('movement_type', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        return context


@login_required
@role_required(['gerente', 'administrador'])
def import_products(request):
    """Importar productos desde Excel"""
    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            result = import_products_from_excel(file, request.user)
            
            if result['errors']:
                for error in result['errors']:
                    messages.error(request, error)
            
            if result['created'] > 0:
                messages.success(request, f'{result["created"]} productos creados.')
            if result['updated'] > 0:
                messages.success(request, f'{result["updated"]} productos actualizados.')
            
            return redirect('stock:product_list')
    else:
        form = ImportExcelForm()
    
    return render(request, 'stock/import_products.html', {'form': form})


@login_required
def product_search_ajax(request):
    """Búsqueda AJAX de productos"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(sku__icontains=query),
        is_active=True
    ).order_by('name')[:10]
    
    results = [{
        'id': p.id,
        'name': p.name,
        'sku': p.sku,
        'price': str(p.price),
        'stock': p.stock_quantity
    } for p in products]
    
    return JsonResponse({'results': results})
