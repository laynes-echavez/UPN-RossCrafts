from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    # Proveedores
    path('proveedores/', views.SupplierListView.as_view(), name='supplier_list'),
    path('proveedores/nuevo/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('proveedores/<int:pk>/editar/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('proveedores/<int:pk>/detalle/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    
    # Órdenes de compra
    path('compras/', views.PurchaseOrderListView.as_view(), name='purchase_order_list'),
    path('compras/nueva/', views.PurchaseOrderCreateView.as_view(), name='purchase_order_create'),
    path('compras/<int:pk>/detalle/', views.PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),
    path('compras/<int:pk>/recibir/', views.purchase_order_receive, name='purchase_order_receive'),
    path('compras/<int:pk>/cancelar/', views.purchase_order_cancel, name='purchase_order_cancel'),
    path('compras/exportar/', views.purchase_order_export, name='purchase_order_export'),
]
