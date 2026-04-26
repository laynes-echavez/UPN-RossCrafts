from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    # Tienda
    path('', views.store_home, name='home'),
    path('tienda/', views.store_catalog, name='catalog'),
    path('tienda/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Carrito
    path('carrito/', views.cart_view, name='cart'),
    path('carrito/agregar/', views.cart_add, name='cart_add'),
    path('carrito/actualizar/', views.cart_update, name='cart_update'),
    path('carrito/eliminar/', views.cart_remove, name='cart_remove'),
    path('carrito/contador/', views.cart_count, name='cart_count'),
    
    # Autenticación de clientes
    path('cuenta/registro/', views.customer_register, name='customer_register'),
    path('cuenta/login/', views.customer_login, name='customer_login'),
    path('cuenta/logout/', views.customer_logout, name='customer_logout'),
    
    # Cuenta de cliente
    path('cuenta/perfil/', views.customer_profile, name='customer_profile'),
    path('cuenta/mis-pedidos/', views.customer_orders, name='customer_orders'),
    path('cuenta/mis-pedidos/<int:pk>/', views.customer_order_detail, name='customer_order_detail'),
    path('cuenta/cambiar-contrasena/', views.customer_change_password, name='customer_change_password'),
    
    # Recuperación de contraseña
    path('cuenta/recuperar-contrasena/', views.customer_password_reset, name='customer_password_reset'),
    path('cuenta/reset/<uidb64>/<token>/', views.customer_password_reset_confirm, name='customer_password_reset_confirm'),
]
