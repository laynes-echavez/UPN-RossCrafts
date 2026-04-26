"""
Script para crear usuarios de prueba en Ross Crafts
Ejecutar: python manage.py shell < create_test_users.py
"""

from django.contrib.auth import get_user_model
from apps.customers.models import Customer

User = get_user_model()

print("=" * 60)
print("CREANDO USUARIOS DE PRUEBA - ROSS CRAFTS")
print("=" * 60)

# ============================================
# EMPLEADOS DEL SISTEMA (User model)
# ============================================

print("\n📋 CREANDO EMPLEADOS DEL SISTEMA...")

# 1. GERENTE
gerente, created = User.objects.get_or_create(
    username='gerente',
    defaults={
        'email': 'gerente@rosscrafts.com',
        'first_name': 'Carlos',
        'last_name': 'Rodríguez',
        'role': 'gerente',
        'phone': '987654321',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    gerente.set_password('gerente123')
    gerente.save()
    print(f"✅ Gerente creado: {gerente.username}")
else:
    print(f"ℹ️  Gerente ya existe: {gerente.username}")

# 2. ADMINISTRADOR
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@rosscrafts.com',
        'first_name': 'María',
        'last_name': 'González',
        'role': 'administrador',
        'phone': '987654322',
        'is_staff': True,
        'is_superuser': False,
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print(f"✅ Administrador creado: {admin.username}")
else:
    print(f"ℹ️  Administrador ya existe: {admin.username}")

# 3. EMPLEADO 1
empleado1, created = User.objects.get_or_create(
    username='empleado1',
    defaults={
        'email': 'empleado1@rosscrafts.com',
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'role': 'empleado',
        'phone': '987654323',
        'is_staff': True,
        'is_superuser': False,
    }
)
if created:
    empleado1.set_password('empleado123')
    empleado1.save()
    print(f"✅ Empleado creado: {empleado1.username}")
else:
    print(f"ℹ️  Empleado ya existe: {empleado1.username}")

# 4. EMPLEADO 2
empleado2, created = User.objects.get_or_create(
    username='empleado2',
    defaults={
        'email': 'empleado2@rosscrafts.com',
        'first_name': 'Ana',
        'last_name': 'Torres',
        'role': 'empleado',
        'phone': '987654324',
        'is_staff': True,
        'is_superuser': False,
    }
)
if created:
    empleado2.set_password('empleado123')
    empleado2.save()
    print(f"✅ Empleado creado: {empleado2.username}")
else:
    print(f"ℹ️  Empleado ya existe: {empleado2.username}")

# ============================================
# CLIENTES DEL ECOMMERCE (Customer model)
# ============================================

print("\n🛒 CREANDO CLIENTES DEL ECOMMERCE...")

# 1. CLIENTE 1
cliente1, created = Customer.objects.get_or_create(
    email='juan.cliente@gmail.com',
    defaults={
        'first_name': 'Juan',
        'last_name': 'Martínez',
        'phone': '999888777',
        'dni': '12345678',
        'address': 'Av. Los Artesanos 123, Trujillo',
        'is_active': True,
        'is_verified': True,
    }
)
if created:
    cliente1.set_password('cliente123')
    cliente1.save()
    print(f"✅ Cliente creado: {cliente1.email}")
else:
    print(f"ℹ️  Cliente ya existe: {cliente1.email}")

# 2. CLIENTE 2
cliente2, created = Customer.objects.get_or_create(
    email='maria.cliente@gmail.com',
    defaults={
        'first_name': 'María',
        'last_name': 'López',
        'phone': '999888666',
        'dni': '87654321',
        'address': 'Jr. Las Flores 456, Trujillo',
        'is_active': True,
        'is_verified': True,
    }
)
if created:
    cliente2.set_password('cliente123')
    cliente2.save()
    print(f"✅ Cliente creado: {cliente2.email}")
else:
    print(f"ℹ️  Cliente ya existe: {cliente2.email}")

# 3. CLIENTE 3
cliente3, created = Customer.objects.get_or_create(
    email='pedro.cliente@gmail.com',
    defaults={
        'first_name': 'Pedro',
        'last_name': 'Sánchez',
        'phone': '999888555',
        'dni': '11223344',
        'address': 'Calle Los Pinos 789, Trujillo',
        'is_active': True,
        'is_verified': True,
    }
)
if created:
    cliente3.set_password('cliente123')
    cliente3.save()
    print(f"✅ Cliente creado: {cliente3.email}")
else:
    print(f"ℹ️  Cliente ya existe: {cliente3.email}")

# 4. CLIENTE 4
cliente4, created = Customer.objects.get_or_create(
    email='lucia.cliente@gmail.com',
    defaults={
        'first_name': 'Lucía',
        'last_name': 'Ramírez',
        'phone': '999888444',
        'dni': '55667788',
        'address': 'Av. La Marina 321, Trujillo',
        'is_active': True,
        'is_verified': True,
    }
)
if created:
    cliente4.set_password('cliente123')
    cliente4.save()
    print(f"✅ Cliente creado: {cliente4.email}")
else:
    print(f"ℹ️  Cliente ya existe: {cliente4.email}")

# 5. CLIENTE 5
cliente5, created = Customer.objects.get_or_create(
    email='carlos.cliente@gmail.com',
    defaults={
        'first_name': 'Carlos',
        'last_name': 'Vega',
        'phone': '999888333',
        'dni': '99887766',
        'address': 'Jr. Independencia 654, Trujillo',
        'is_active': True,
        'is_verified': True,
    }
)
if created:
    cliente5.set_password('cliente123')
    cliente5.save()
    print(f"✅ Cliente creado: {cliente5.email}")
else:
    print(f"ℹ️  Cliente ya existe: {cliente5.email}")

# ============================================
# RESUMEN
# ============================================

print("\n" + "=" * 60)
print("✅ USUARIOS CREADOS EXITOSAMENTE")
print("=" * 60)

print("\n📊 RESUMEN:")
print(f"   Empleados del sistema: {User.objects.count()}")
print(f"   Clientes del ecommerce: {Customer.objects.count()}")

print("\n" + "=" * 60)
print("CREDENCIALES DE ACCESO")
print("=" * 60)

print("\n🔐 EMPLEADOS DEL SISTEMA (Admin Panel)")
print("-" * 60)
print("URL: http://127.0.0.1:8000/auth/login/")
print()
print("GERENTE:")
print("  Usuario: gerente")
print("  Contraseña: gerente123")
print("  Permisos: Acceso total al sistema")
print()
print("ADMINISTRADOR:")
print("  Usuario: admin")
print("  Contraseña: admin123")
print("  Permisos: Gestión de productos, clientes, ventas")
print()
print("EMPLEADO 1:")
print("  Usuario: empleado1")
print("  Contraseña: empleado123")
print("  Permisos: Ventas, consulta de productos y clientes")
print()
print("EMPLEADO 2:")
print("  Usuario: empleado2")
print("  Contraseña: empleado123")
print("  Permisos: Ventas, consulta de productos y clientes")

print("\n🛒 CLIENTES DEL ECOMMERCE")
print("-" * 60)
print("URL: http://127.0.0.1:8000/cuenta/login/")
print()
print("CLIENTE 1:")
print("  Email: juan.cliente@gmail.com")
print("  Contraseña: cliente123")
print()
print("CLIENTE 2:")
print("  Email: maria.cliente@gmail.com")
print("  Contraseña: cliente123")
print()
print("CLIENTE 3:")
print("  Email: pedro.cliente@gmail.com")
print("  Contraseña: cliente123")
print()
print("CLIENTE 4:")
print("  Email: lucia.cliente@gmail.com")
print("  Contraseña: cliente123")
print()
print("CLIENTE 5:")
print("  Email: carlos.cliente@gmail.com")
print("  Contraseña: cliente123")

print("\n" + "=" * 60)
print("✨ ¡Listo para probar!")
print("=" * 60)
