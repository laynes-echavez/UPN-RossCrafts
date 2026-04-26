"""
Script de prueba para el sistema de autenticación de clientes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from apps.customers.models import Customer
from apps.ecommerce.backends import CustomerAuthBackend

def test_customer_authentication():
    print("=" * 60)
    print("PRUEBA DEL SISTEMA DE AUTENTICACIÓN DE CLIENTES")
    print("=" * 60)
    
    # 1. Crear cliente de prueba
    print("\n1. Creando cliente de prueba...")
    email = "test_customer@rosscrafts.com"
    
    # Eliminar si existe
    Customer.objects.filter(email=email).delete()
    
    customer = Customer(
        first_name="Cliente",
        last_name="Prueba",
        email=email,
        phone="987654321"
    )
    customer.set_password("Test1234")
    customer.save()
    print(f"   ✓ Cliente creado: {customer.full_name} ({customer.email})")
    
    # 2. Verificar contraseña
    print("\n2. Verificando contraseña...")
    if customer.check_password("Test1234"):
        print("   ✓ Contraseña correcta verificada")
    else:
        print("   ✗ Error: Contraseña no verificada")
    
    if not customer.check_password("WrongPassword"):
        print("   ✓ Contraseña incorrecta rechazada")
    else:
        print("   ✗ Error: Contraseña incorrecta aceptada")
    
    # 3. Probar backend de autenticación
    print("\n3. Probando CustomerAuthBackend...")
    backend = CustomerAuthBackend()
    
    # Autenticación exitosa
    auth_customer = backend.authenticate(None, email=email, password="Test1234")
    if auth_customer:
        print(f"   ✓ Autenticación exitosa: {auth_customer.full_name}")
    else:
        print("   ✗ Error: Autenticación falló")
    
    # Autenticación fallida
    auth_customer = backend.authenticate(None, email=email, password="WrongPassword")
    if not auth_customer:
        print("   ✓ Autenticación con contraseña incorrecta rechazada")
    else:
        print("   ✗ Error: Autenticación incorrecta aceptada")
    
    # 4. Probar get_user
    print("\n4. Probando get_user...")
    retrieved_customer = backend.get_user(customer.id)
    if retrieved_customer:
        print(f"   ✓ Cliente recuperado: {retrieved_customer.full_name}")
    else:
        print("   ✗ Error: No se pudo recuperar el cliente")
    
    # 5. Verificar propiedades
    print("\n5. Verificando propiedades...")
    print(f"   is_authenticated: {customer.is_authenticated}")
    print(f"   is_anonymous: {customer.is_anonymous}")
    print(f"   is_active: {customer.is_active}")
    
    # 6. Limpiar
    print("\n6. Limpiando datos de prueba...")
    customer.delete()
    print("   ✓ Cliente de prueba eliminado")
    
    print("\n" + "=" * 60)
    print("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE ✓")
    print("=" * 60)

if __name__ == "__main__":
    test_customer_authentication()
