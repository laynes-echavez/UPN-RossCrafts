"""
Script para poblar la base de datos con datos de prueba
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from apps.stock.models import Category, Product
from apps.customers.models import Customer
from apps.suppliers.models import Supplier
from apps.authentication.models import User

print("=" * 60)
print("POBLANDO BASE DE DATOS CON DATOS DE PRUEBA")
print("=" * 60)

# Crear categorías
print("\n📦 Creando categorías...")
categories_data = [
    {"name": "Artesanías", "description": "Productos artesanales hechos a mano"},
    {"name": "Textiles", "description": "Productos textiles y tejidos"},
    {"name": "Cerámica", "description": "Productos de cerámica y alfarería"},
    {"name": "Joyería", "description": "Joyería artesanal"},
    {"name": "Decoración", "description": "Artículos decorativos"},
]

categories = []
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data["name"],
        defaults={"description": cat_data["description"]}
    )
    categories.append(cat)
    status = "✓ Creada" if created else "○ Ya existe"
    print(f"  {status}: {cat.name}")

# Crear productos
print("\n🛍️  Creando productos...")
products_data = [
    {"name": "Bolso Artesanal", "sku": "BOLSO001", "category": categories[1], "price": 150.00, "cost_price": 75.00, "stock": 20},
    {"name": "Collar de Plata", "sku": "COLLAR001", "category": categories[3], "price": 200.00, "cost_price": 100.00, "stock": 15},
    {"name": "Jarrón de Cerámica", "sku": "JARRON001", "category": categories[2], "price": 120.00, "cost_price": 60.00, "stock": 10},
    {"name": "Tapiz Decorativo", "sku": "TAPIZ001", "category": categories[4], "price": 180.00, "cost_price": 90.00, "stock": 8},
    {"name": "Pulsera Artesanal", "sku": "PULSERA001", "category": categories[3], "price": 80.00, "cost_price": 40.00, "stock": 30},
    {"name": "Plato Decorativo", "sku": "PLATO001", "category": categories[2], "price": 60.00, "cost_price": 30.00, "stock": 25},
    {"name": "Bufanda Tejida", "sku": "BUFANDA001", "category": categories[1], "price": 90.00, "cost_price": 45.00, "stock": 18},
    {"name": "Figura Decorativa", "sku": "FIGURA001", "category": categories[0], "price": 110.00, "cost_price": 55.00, "stock": 12},
]

for prod_data in products_data:
    prod, created = Product.objects.get_or_create(
        sku=prod_data["sku"],
        defaults={
            "name": prod_data["name"],
            "category": prod_data["category"],
            "price": prod_data["price"],
            "cost_price": prod_data["cost_price"],
            "stock_quantity": prod_data["stock"],
            "min_stock_quantity": 5,
        }
    )
    status = "✓ Creado" if created else "○ Ya existe"
    print(f"  {status}: {prod.name} (SKU: {prod.sku}) - Stock: {prod.stock_quantity}")

# Crear clientes
print("\n👥 Creando clientes...")
customers_data = [
    {"first_name": "Juan", "last_name": "Pérez", "email": "juan.perez@example.com", "phone": "987654321", "dni": "12345678"},
    {"first_name": "María", "last_name": "García", "email": "maria.garcia@example.com", "phone": "987654322", "dni": "23456789"},
    {"first_name": "Carlos", "last_name": "López", "email": "carlos.lopez@example.com", "phone": "987654323", "dni": "34567890"},
    {"first_name": "Ana", "last_name": "Martínez", "email": "ana.martinez@example.com", "phone": "987654324", "dni": "45678901"},
    {"first_name": "Luis", "last_name": "Rodríguez", "email": "luis.rodriguez@example.com", "phone": "987654325", "dni": "56789012"},
]

for cust_data in customers_data:
    cust, created = Customer.objects.get_or_create(
        email=cust_data["email"],
        defaults=cust_data
    )
    status = "✓ Creado" if created else "○ Ya existe"
    print(f"  {status}: {cust.full_name} ({cust.email})")

# Crear proveedores
print("\n🏭 Creando proveedores...")
suppliers_data = [
    {"company_name": "Artesanías del Sur", "contact_name": "Pedro Sánchez", "email": "contacto@artesaniassur.com", "phone": "987111111", "ruc": "20123456789"},
    {"company_name": "Textiles Andinos", "contact_name": "Rosa Flores", "email": "ventas@textilesandinos.com", "phone": "987222222", "ruc": "20234567890"},
    {"company_name": "Cerámica Tradicional", "contact_name": "Miguel Torres", "email": "info@ceramicatrad.com", "phone": "987333333", "ruc": "20345678901"},
]

for supp_data in suppliers_data:
    supp, created = Supplier.objects.get_or_create(
        ruc=supp_data["ruc"],
        defaults=supp_data
    )
    status = "✓ Creado" if created else "○ Ya existe"
    print(f"  {status}: {supp.company_name} (RUC: {supp.ruc})")

# Resumen
print("\n" + "=" * 60)
print("RESUMEN DE DATOS CREADOS")
print("=" * 60)
print(f"  Categorías: {Category.objects.count()}")
print(f"  Productos: {Product.objects.count()}")
print(f"  Clientes: {Customer.objects.count()}")
print(f"  Proveedores: {Supplier.objects.count()}")
print(f"  Usuarios: {User.objects.count()}")
print("=" * 60)
print("\n✓ Datos de prueba cargados exitosamente")
print("\nPara crear un superusuario, ejecuta:")
print("  python manage.py createsuperuser")
