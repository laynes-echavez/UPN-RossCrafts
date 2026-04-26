"""
Script para probar el módulo de Proveedores y Órdenes de Compra
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from apps.suppliers.models import Supplier, PurchaseOrder, PurchaseOrderItem
from apps.stock.models import Product, StockMovement
from apps.authentication.models import User
from decimal import Decimal


def test_suppliers_module():
    print("=" * 60)
    print("PRUEBA DEL MÓDULO DE PROVEEDORES Y ÓRDENES DE COMPRA")
    print("=" * 60)
    
    # 1. Crear proveedores de prueba
    print("\n1. Creando proveedores de prueba...")
    
    suppliers_data = [
        {
            'company_name': 'Artesanías del Perú SAC',
            'contact_name': 'María González',
            'email': 'contacto@artesaniasperu.com',
            'phone': '987654321',
            'ruc': '20123456789',
            'address': 'Av. Los Artesanos 123, Lima'
        },
        {
            'company_name': 'Textiles Andinos EIRL',
            'contact_name': 'Carlos Ramírez',
            'email': 'ventas@textilesandinos.com',
            'phone': '987654322',
            'ruc': '20234567890',
            'address': 'Jr. Cusco 456, Arequipa'
        },
        {
            'company_name': 'Cerámica Tradicional SA',
            'contact_name': 'Ana Torres',
            'email': 'info@ceramicatradicional.com',
            'phone': '987654323',
            'ruc': '20345678901',
            'address': 'Calle Artesanos 789, Ayacucho'
        }
    ]
    
    for data in suppliers_data:
        supplier, created = Supplier.objects.get_or_create(
            ruc=data['ruc'],
            defaults=data
        )
        if created:
            print(f"   ✓ Proveedor creado: {supplier.company_name}")
        else:
            print(f"   - Proveedor ya existe: {supplier.company_name}")
    
    # 2. Verificar proveedores
    print("\n2. Verificando proveedores registrados...")
    suppliers = Supplier.objects.filter(is_active=True)
    print(f"   ✓ Total de proveedores activos: {suppliers.count()}")
    
    for supplier in suppliers[:3]:
        print(f"     - {supplier.company_name} (RUC: {supplier.ruc})")
    
    # 3. Crear orden de compra de prueba
    print("\n3. Creando orden de compra de prueba...")
    
    # Obtener usuario administrador
    admin_user = User.objects.filter(role='administrador').first()
    if not admin_user:
        print("   ⚠ No hay usuario administrador disponible")
        return
    
    # Obtener proveedor
    supplier = suppliers.first()
    
    # Obtener productos
    products = Product.objects.filter(is_active=True)[:3]
    
    if products.count() < 2:
        print("   ⚠ No hay suficientes productos para crear la orden")
        return
    
    # Crear orden de compra
    order = PurchaseOrder.objects.create(
        supplier=supplier,
        status='pending',
        notes='Orden de prueba para reabastecimiento'
    )
    
    print(f"   ✓ Orden creada: OC-{order.id}")
    print(f"   Proveedor: {supplier.company_name}")
    
    # Agregar items a la orden
    total = Decimal('0')
    
    for product in products:
        quantity = 10
        unit_cost = product.cost_price
        subtotal = quantity * unit_cost
        
        PurchaseOrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_cost=unit_cost,
            subtotal=subtotal
        )
        
        total += subtotal
        print(f"     - {product.name} x {quantity} @ S/. {unit_cost} = S/. {subtotal}")
    
    # Actualizar total de la orden
    order.total = total
    order.save()
    
    print(f"   Total de la orden: S/. {total:.2f}")
    
    # 4. Simular recepción de orden
    print("\n4. Simulando recepción de orden...")
    
    # Guardar stock anterior
    stock_before = {}
    for item in order.items.all():
        stock_before[item.product.id] = item.product.stock_quantity
    
    # Marcar como recibida
    order.status = 'received'
    order.save()
    
    # Crear movimientos de stock
    for item in order.items.all():
        StockMovement.objects.create(
            product=item.product,
            user=admin_user,
            movement_type='entrada',
            quantity=item.quantity,
            reason=f'OC #{order.id} recibida'
        )
    
    print(f"   ✓ Orden OC-{order.id} marcada como recibida")
    
    # Verificar actualización de stock
    print("\n   Stock actualizado:")
    for item in order.items.all():
        item.product.refresh_from_db()
        stock_after = item.product.stock_quantity
        stock_diff = stock_after - stock_before[item.product.id]
        print(f"     - {item.product.name}: {stock_before[item.product.id]} → {stock_after} (+{stock_diff})")
    
    # 5. Verificar órdenes de compra
    print("\n5. Verificando órdenes de compra...")
    orders = PurchaseOrder.objects.all().order_by('-created_at')
    print(f"   ✓ Total de órdenes: {orders.count()}")
    
    print("\n   Últimas 5 órdenes:")
    for order in orders[:5]:
        print(f"     - OC-{order.id} | {order.supplier.company_name} | "
              f"{order.get_status_display()} | S/. {order.total:.2f} | "
              f"{order.created_at.strftime('%d/%m/%Y')}")
    
    # 6. Estadísticas por proveedor
    print("\n6. Estadísticas por proveedor:")
    for supplier in suppliers[:3]:
        orders_count = PurchaseOrder.objects.filter(supplier=supplier).count()
        received_orders = PurchaseOrder.objects.filter(
            supplier=supplier,
            status='received'
        )
        total_spent = sum(order.total for order in received_orders)
        pending_orders = PurchaseOrder.objects.filter(
            supplier=supplier,
            status='pending'
        ).count()
        
        print(f"\n   {supplier.company_name}:")
        print(f"     - Total de órdenes: {orders_count}")
        print(f"     - Órdenes pendientes: {pending_orders}")
        print(f"     - Total gastado: S/. {total_spent:.2f}")
    
    # 7. Verificar movimientos de stock
    print("\n7. Verificando movimientos de stock tipo 'entrada'...")
    movements = StockMovement.objects.filter(
        movement_type='entrada'
    ).order_by('-created_at')[:5]
    
    print(f"   ✓ Total de movimientos de entrada: {StockMovement.objects.filter(movement_type='entrada').count()}")
    print("\n   Últimos 5 movimientos:")
    for mov in movements:
        print(f"     - {mov.product.name} | +{mov.quantity} unidades | "
              f"{mov.reason} | {mov.created_at.strftime('%d/%m/%Y %H:%M')}")
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)
    print("\nPara probar el módulo en el navegador:")
    print("1. Inicia el servidor: python manage.py runserver")
    print("2. Accede a:")
    print("   - Proveedores: http://localhost:8000/proveedores/")
    print("   - Órdenes de Compra: http://localhost:8000/compras/")
    print("3. Inicia sesión con un usuario administrador o gerente")
    print("   - Usuario: admin / Contraseña: Ross2026!")
    print("   - Usuario: gerente / Contraseña: Ross2026!")
    print("\n")


if __name__ == '__main__':
    test_suppliers_module()
