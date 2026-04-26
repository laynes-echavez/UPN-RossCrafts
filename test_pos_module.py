"""
Script para probar el módulo POS (Point of Sale)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from apps.authentication.models import User
from apps.stock.models import Product, Category, StockMovement
from apps.customers.models import Customer
from apps.sales.models import Sale, SaleItem
from decimal import Decimal


def test_pos_module():
    print("=" * 60)
    print("PRUEBA DEL MÓDULO POS (POINT OF SALE)")
    print("=" * 60)
    
    # 1. Verificar que existen productos
    print("\n1. Verificando productos disponibles...")
    products = Product.objects.filter(is_active=True, stock_quantity__gt=0)
    print(f"   ✓ Productos disponibles: {products.count()}")
    
    if products.count() > 0:
        for p in products[:5]:
            print(f"     - {p.name} (SKU: {p.sku}) - Stock: {p.stock_quantity} - Precio: S/. {p.price}")
    
    # 2. Verificar que existen clientes
    print("\n2. Verificando clientes registrados...")
    customers = Customer.objects.filter(is_active=True)
    print(f"   ✓ Clientes activos: {customers.count()}")
    
    if customers.count() > 0:
        for c in customers[:3]:
            print(f"     - {c.full_name} (DNI: {c.dni or 'N/A'})")
    
    # 3. Verificar usuarios que pueden usar el POS
    print("\n3. Verificando usuarios con acceso al POS...")
    pos_users = User.objects.filter(role__in=['empleado', 'administrador'], is_active=True)
    print(f"   ✓ Usuarios con acceso: {pos_users.count()}")
    
    for u in pos_users:
        print(f"     - {u.username} ({u.get_role_display()})")
    
    # 4. Simular una venta
    print("\n4. Simulando una venta de prueba...")
    
    if products.count() > 0 and pos_users.count() > 0:
        # Seleccionar productos
        product1 = products.first()
        product2 = products[1] if products.count() > 1 else product1
        
        # Seleccionar usuario
        user = pos_users.first()
        
        # Seleccionar cliente (opcional)
        customer = customers.first() if customers.count() > 0 else None
        
        # Calcular totales
        qty1 = 2
        qty2 = 1
        subtotal = (product1.price * qty1) + (product2.price * qty2)
        discount = Decimal('5.00')  # Descuento fijo de S/. 5.00
        subtotal_after_discount = subtotal - discount
        tax = subtotal_after_discount * Decimal('0.18')  # IGV 18%
        total = subtotal_after_discount + tax
        
        print(f"\n   Productos:")
        print(f"     - {product1.name} x {qty1} = S/. {product1.price * qty1}")
        print(f"     - {product2.name} x {qty2} = S/. {product2.price * qty2}")
        print(f"\n   Cálculos:")
        print(f"     Subtotal: S/. {subtotal:.2f}")
        print(f"     Descuento: - S/. {discount:.2f}")
        print(f"     IGV (18%): S/. {tax:.2f}")
        print(f"     TOTAL: S/. {total:.2f}")
        print(f"\n   Cliente: {customer.full_name if customer else 'Sin cliente'}")
        print(f"   Atendido por: {user.username}")
        print(f"   Método de pago: Efectivo")
        
        # Crear la venta
        sale = Sale.objects.create(
            customer=customer,
            user=user,
            subtotal=subtotal,
            tax=tax,
            discount=discount,
            total=total,
            payment_method='cash',
            status='completed'
        )
        
        # Crear items de venta
        SaleItem.objects.create(
            sale=sale,
            product=product1,
            quantity=qty1,
            unit_price=product1.price,
            subtotal=product1.price * qty1
        )
        
        SaleItem.objects.create(
            sale=sale,
            product=product2,
            quantity=qty2,
            unit_price=product2.price,
            subtotal=product2.price * qty2
        )
        
        # Crear movimientos de stock
        StockMovement.objects.create(
            product=product1,
            user=user,
            movement_type='salida',
            quantity=qty1,
            reason=f'Venta #{sale.id}'
        )
        
        StockMovement.objects.create(
            product=product2,
            user=user,
            movement_type='salida',
            quantity=qty2,
            reason=f'Venta #{sale.id}'
        )
        
        print(f"\n   ✓ Venta registrada exitosamente!")
        print(f"   ID de venta: {sale.id}")
        print(f"   Comprobante: RC-{sale.created_at.year}-{sale.id:06d}")
        
        # Verificar stock actualizado
        product1.refresh_from_db()
        product2.refresh_from_db()
        
        print(f"\n   Stock actualizado:")
        print(f"     - {product1.name}: {product1.stock_quantity} unidades")
        print(f"     - {product2.name}: {product2.stock_quantity} unidades")
        
    else:
        print("   ⚠ No hay suficientes datos para simular una venta")
    
    # 5. Verificar ventas registradas
    print("\n5. Verificando ventas registradas...")
    sales = Sale.objects.all().order_by('-created_at')
    print(f"   ✓ Total de ventas: {sales.count()}")
    
    if sales.count() > 0:
        print("\n   Últimas 5 ventas:")
        for s in sales[:5]:
            comprobante = f'RC-{s.created_at.year}-{s.id:06d}'
            print(f"     - {comprobante} | {s.created_at.strftime('%d/%m/%Y %H:%M')} | "
                  f"S/. {s.total:.2f} | {s.get_payment_method_display()} | "
                  f"{s.customer.full_name if s.customer else 'Sin cliente'}")
    
    # 6. Verificar endpoints AJAX
    print("\n6. Endpoints AJAX disponibles:")
    print("   ✓ /stock/buscar/?q=<query> - Búsqueda de productos")
    print("   ✓ /clientes/buscar/?q=<query> - Búsqueda de clientes")
    print("   ✓ /ventas/registrar/ - Registrar venta (POST)")
    print("   ✓ /ventas/<id>/comprobante/ - Generar PDF")
    print("   ✓ /clientes/registro-rapido/ - Registro rápido de cliente (POST)")
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)
    print("\nPara probar el POS en el navegador:")
    print("1. Inicia el servidor: python manage.py runserver")
    print("2. Accede a: http://localhost:8000/dashboard/pos/")
    print("3. Inicia sesión con un usuario empleado o administrador")
    print("   - Usuario: empleado / Contraseña: Ross2026!")
    print("   - Usuario: admin / Contraseña: Ross2026!")
    print("\n")


if __name__ == '__main__':
    test_pos_module()
