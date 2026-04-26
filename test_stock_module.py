"""
Script para probar el módulo de stock
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from apps.stock.models import Product, Category, StockMovement
from apps.authentication.models import User
from django.db.models import F

print("=" * 60)
print("PRUEBA DEL MÓDULO DE STOCK")
print("=" * 60)

# Verificar productos
print("\n📦 PRODUCTOS REGISTRADOS:")
print("-" * 60)
products = Product.objects.all().order_by('name')[:10]
for product in products:
    stock_status = "⚠️ BAJO" if product.needs_restock else "✓ OK"
    print(f"  {product.sku:<15} | {product.name:<30} | Stock: {product.stock_quantity:>3} {stock_status}")

# Verificar categorías
print(f"\n📂 CATEGORÍAS:")
print("-" * 60)
categories = Category.objects.all().order_by('name')
for category in categories:
    product_count = category.products.count()
    print(f"  {category.name:<20} | {product_count} productos")

# Verificar movimientos
print(f"\n📊 MOVIMIENTOS DE STOCK (Últimos 10):")
print("-" * 60)
movements = StockMovement.objects.all().order_by('-created_at')[:10]
if movements:
    for movement in movements:
        print(f"  {movement.created_at.strftime('%Y-%m-%d %H:%M')} | {movement.product.name:<25} | {movement.movement_type:<8} | Qty: {movement.quantity:>3}")
else:
    print("  No hay movimientos registrados aún")

# Verificar stock bajo
print(f"\n⚠️  ALERTA DE STOCK BAJO:")
print("-" * 60)
low_stock = Product.objects.filter(
    is_active=True,
    stock_quantity__lte=F('min_stock_quantity')
).order_by('stock_quantity')

if low_stock:
    for product in low_stock:
        print(f"  {product.name:<30} | Stock: {product.stock_quantity} / Mínimo: {product.min_stock_quantity}")
else:
    print("  ✓ Todos los productos tienen stock suficiente")

# Estadísticas
print("\n" + "=" * 60)
print("ESTADÍSTICAS")
print("=" * 60)
print(f"  Total de productos: {Product.objects.count()}")
print(f"  Productos activos: {Product.objects.filter(is_active=True).count()}")
print(f"  Productos con stock bajo: {low_stock.count()}")
print(f"  Total de categorías: {Category.objects.count()}")
print(f"  Total de movimientos: {StockMovement.objects.count()}")

# URLs para probar
print("\n" + "=" * 60)
print("URLS PARA PROBAR")
print("=" * 60)
print("  Lista de productos: http://localhost:8000/stock/productos/")
print("  Nuevo producto: http://localhost:8000/stock/productos/nuevo/")
print("  Categorías: http://localhost:8000/stock/categorias/")
print("  Movimientos: http://localhost:8000/stock/movimientos/")
print("  Importar Excel: http://localhost:8000/stock/importar/")
print("  Stock bajo: http://localhost:8000/stock/productos/?stock_level=low")

print("\n✓ Módulo de stock listo para usar")
print("  Ejecuta: python manage.py runserver")
