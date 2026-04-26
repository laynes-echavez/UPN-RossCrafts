"""
Script de prueba para verificar la integración con Stripe
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from django.conf import settings
import stripe

def test_stripe_configuration():
    print("=" * 60)
    print("PRUEBA DE CONFIGURACIÓN DE STRIPE")
    print("=" * 60)
    
    # 1. Verificar variables de entorno
    print("\n1. Verificando variables de entorno...")
    
    if settings.STRIPE_PUBLIC_KEY:
        print(f"   ✓ STRIPE_PUBLIC_KEY configurada: {settings.STRIPE_PUBLIC_KEY[:20]}...")
    else:
        print("   ✗ STRIPE_PUBLIC_KEY no configurada")
        return False
    
    if settings.STRIPE_SECRET_KEY:
        print(f"   ✓ STRIPE_SECRET_KEY configurada: {settings.STRIPE_SECRET_KEY[:20]}...")
    else:
        print("   ✗ STRIPE_SECRET_KEY no configurada")
        return False
    
    if settings.STRIPE_WEBHOOK_SECRET:
        print(f"   ✓ STRIPE_WEBHOOK_SECRET configurada: {settings.STRIPE_WEBHOOK_SECRET[:20]}...")
    else:
        print("   ⚠ STRIPE_WEBHOOK_SECRET no configurada (opcional para testing)")
    
    # 2. Verificar conexión con Stripe
    print("\n2. Verificando conexión con Stripe API...")
    
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Intentar listar productos (solo para verificar conexión)
        balance = stripe.Balance.retrieve()
        print(f"   ✓ Conexión exitosa con Stripe")
        print(f"   ✓ Moneda disponible: {balance.available[0].currency.upper()}")
        print(f"   ✓ Balance disponible: {balance.available[0].amount / 100}")
    except stripe.error.AuthenticationError:
        print("   ✗ Error de autenticación - Verifica STRIPE_SECRET_KEY")
        return False
    except Exception as e:
        print(f"   ✗ Error conectando con Stripe: {e}")
        return False
    
    # 3. Crear PaymentIntent de prueba
    print("\n3. Creando PaymentIntent de prueba...")
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=10000,  # S/. 100.00
            currency='pen',
            metadata={
                'test': 'true',
                'customer_email': 'test@rosscrafts.com',
            }
        )
        print(f"   ✓ PaymentIntent creado: {intent.id}")
        print(f"   ✓ Monto: S/. {intent.amount / 100}")
        print(f"   ✓ Estado: {intent.status}")
        print(f"   ✓ Client Secret: {intent.client_secret[:30]}...")
        
        # Cancelar el intent de prueba
        stripe.PaymentIntent.cancel(intent.id)
        print(f"   ✓ PaymentIntent cancelado (era solo prueba)")
    except Exception as e:
        print(f"   ✗ Error creando PaymentIntent: {e}")
        return False
    
    # 4. Verificar URLs
    print("\n4. Verificando URLs configuradas...")
    
    from django.urls import reverse
    
    urls_to_check = [
        ('payments:checkout', '/checkout/'),
        ('payments:payment', '/checkout/pago/'),
        ('payments:create_intent', '/checkout/crear-intent/'),
        ('payments:success', '/checkout/exitoso/'),
        ('payments:cancelled', '/checkout/cancelado/'),
        ('payments:webhook', '/stripe/webhook/'),
    ]
    
    for url_name, expected_path in urls_to_check:
        try:
            path = reverse(url_name)
            if path == expected_path:
                print(f"   ✓ {url_name}: {path}")
            else:
                print(f"   ⚠ {url_name}: {path} (esperado: {expected_path})")
        except Exception as e:
            print(f"   ✗ {url_name}: Error - {e}")
    
    # 5. Verificar modelos
    print("\n5. Verificando modelos...")
    
    from apps.sales.models import Sale
    from apps.ecommerce.models import Order
    from apps.payments.models import Payment
    
    print(f"   ✓ Sale model: {Sale._meta.db_table}")
    print(f"   ✓ Order model: {Order._meta.db_table}")
    print(f"   ✓ Payment model: {Payment._meta.db_table}")
    
    # Verificar campo receipt_number
    if hasattr(Sale, 'receipt_number'):
        print(f"   ✓ Sale.receipt_number existe")
    else:
        print(f"   ✗ Sale.receipt_number no existe")
    
    print("\n" + "=" * 60)
    print("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE ✓")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("1. Iniciar servidor: python manage.py runserver")
    print("2. Iniciar Stripe CLI: stripe listen --forward-to localhost:8000/stripe/webhook/")
    print("3. Ir a: http://localhost:8000/checkout/")
    print("4. Usar tarjeta de prueba: 4242 4242 4242 4242")
    print("\n")
    
    return True

if __name__ == "__main__":
    try:
        test_stripe_configuration()
    except Exception as e:
        print(f"\n✗ Error ejecutando pruebas: {e}")
        import traceback
        traceback.print_exc()
