from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Checkout
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/pago/', views.payment_view, name='payment'),
    path('checkout/crear-intent/', views.create_payment_intent, name='create_intent'),
    path('checkout/exitoso/', views.checkout_success, name='success'),
    path('checkout/cancelado/', views.checkout_cancelled, name='cancelled'),
    
    # Stripe webhook
    path('stripe/webhook/', views.stripe_webhook, name='webhook'),
    # Confirmación del lado del cliente
    path('checkout/confirmar/', views.confirm_payment, name='confirm_payment'),
]
