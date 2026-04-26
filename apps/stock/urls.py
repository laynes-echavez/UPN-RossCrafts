from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    # Productos
    path('productos/', views.ProductListView.as_view(), name='product_list'),
    path('productos/nuevo/', views.ProductCreateView.as_view(), name='product_create'),
    path('productos/<int:pk>/editar/', views.ProductUpdateView.as_view(), name='product_update'),
    path('productos/<int:pk>/eliminar/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('productos/<int:pk>/detalle/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Categorías
    path('categorias/', views.CategoryListView.as_view(), name='category_list'),
    
    # Movimientos de stock
    path('movimientos/', views.StockMovementListView.as_view(), name='movement_list'),
    
    # Importación
    path('importar/', views.import_products, name='import_products'),
    
    # Búsqueda AJAX
    path('buscar/', views.product_search_ajax, name='product_search'),
]
