from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('dashboard/pos/', views.pos_view, name='pos'),
    path('ventas/registrar/', views.register_sale, name='register_sale'),
    path('ventas/<int:sale_id>/comprobante/', views.sale_receipt_pdf, name='sale_receipt'),
    path('clientes/registro-rapido/', views.quick_customer_register, name='quick_customer_register'),
]
