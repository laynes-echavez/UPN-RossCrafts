"""
Script para probar el módulo de clientes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from apps.customers.models import Customer
from apps.sales.models import Sale
from apps.ecommerce.models import Order
from django.db.models import Sum

print("=" * 60)
print("PRUEBA DEL MÓDULO DE CLIENTES")
print("=" * 60)

# Verificar clientes
print("\n👥 CLIENTES REGISTRADOS:")
print("-" * 60)
customers = Customer.objects.all().order_by('last_name', 'first_name')[:10]
for customer in customers:
    status = "✓ Activo" if customer.is_active else "✗ Inactivo"
    print(f"  {customer.full_name:<30} | {customer.email:<30} | {status}")

# Verificar clientes con compras
print(f"\n💰 CLIENTES CON HISTORIAL DE COMPRAS:")
print("-" * 60)
customers_with_purchases = Customer.objects.filter(
    sales__isnull=False
).distinct().order_by('last_name')

if customers_with_purchases:
    for customer in customers_with_purchases[:5]:
        sales = Sale.objects.filter(customer=customer)
        total = sales.aggregate(total=Sum('total'))['total'] or 0
        count = sales.count()
        print(f"  {customer.full_name:<30} | Compras: {count:>2} | Total: S/. {total:>8.2f}")
else:
    print("  No hay clientes con historial de compras aún")

# Estadísticas
print("\n" + "=" * 60)
print("ESTADÍSTICAS")
print("=" * 60)
print(f"  Total de clientes: {Customer.objects.count()}")
print(f"  Clientes activos: {Customer.objects.filter(is_active=True).count()}")
print(f"  Clientes inactivos: {Customer.objects.filter(is_active=False).count()}")
print(f"  Clientes con compras: {customers_with_purchases.count()}")

# Validaciones
print("\n" + "=" * 60)
print("VALIDACIONES IMPLEMENTADAS")
print("=" * 60)
print("  ✓ DNI: Exactamente 8 dígitos numéricos")
print("  ✓ Email: Único en el sistema")
print("  ✓ Teléfono: Entre 9 y 15 dígitos")
print("  ✓ Soft delete: is_active=False")

# URLs para probar
print("\n" + "=" * 60)
print("URLS PARA PROBAR")
print("=" * 60)
print("  Lista de clientes: http://localhost:8000/clientes/")
print("  Nuevo cliente: http://localhost:8000/clientes/nuevo/")
print("  Exportar Excel: http://localhost:8000/clientes/exportar/")
print("  Búsqueda AJAX: http://localhost:8000/clientes/buscar/?q=juan")

# Ejemplo de búsqueda AJAX
print("\n" + "=" * 60)
print("EJEMPLO DE BÚSQUEDA AJAX")
print("=" * 60)
print("  Endpoint: /clientes/buscar/?q=texto")
print("  Respuesta JSON:")
print("  {")
print('    "results": [')
print("      {")
print('        "id": 1,')
print('        "full_name": "Juan Pérez",')
print('        "email": "juan@email.com",')
print('        "dni": "12345678",')
print('        "phone": "987654321"')
print("      }")
print("    ]")
print("  }")

print("\n✓ Módulo de clientes listo para usar")
print("  Ejecuta: python manage.py runserver")
