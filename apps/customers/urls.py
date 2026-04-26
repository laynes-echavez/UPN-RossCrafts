from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # Clientes
    path('clientes/', views.CustomerListView.as_view(), name='customer_list'),
    path('clientes/nuevo/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('clientes/<int:pk>/editar/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('clientes/<int:pk>/perfil/', views.CustomerProfileView.as_view(), name='customer_profile'),
    path('clientes/<int:pk>/desactivar/', views.customer_deactivate, name='customer_deactivate'),
    
    # Búsqueda y exportación
    path('clientes/buscar/', views.customer_search_ajax, name='customer_search'),
    path('clientes/exportar/', views.customer_export_excel, name='customer_export'),
]
