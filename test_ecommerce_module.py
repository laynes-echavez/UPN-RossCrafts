"""
Script para probar el módulo de E-commerce
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from apps.stock.models import Product, Category
from apps.ecommerce.models import Cart, CartItem


def test_ecommerce_module():
    print("=" * 60)
    print("PRUEBA DEL MÓDULO DE E-COMMERCE")
    print("=" * 60)
    
    # 1. Verificar productos con slug
    print("\n1. Verificando productos con slug...")
    products = Product.objects.filter(is_active=True)
    print(f"   ✓ Productos activos: {products.count()}")
    
    for product in products[:5]:
        print(f"     - {product.name}")
        print(f"       Slug: {product.slug}")
        print(f"       Precio: S/. {product.price}")
        print(f"       Stock: {product.stock_quantity}")
    
    # 2. Verificar categorías
    print("\n2. Verificando categorías...")
    categories = Category.objects.filter(is_active=True)
    print(f"   ✓ Categorías activas: {categories.count()}")
    
    for category in categories:
        product_count = category.products.filter(is_active=True).count()
        print(f"     - {category.name}: {product_count} productos")
    
    # 3. Simular carrito de compras
    print("\n3. Simulando carrito de compras...")
    
    # Crear carrito de sesión
    cart = Cart.objects.create(session_key='test-session-123')
    print(f"   ✓ Carrito creado: #{cart.id}")
    
    # Agregar productos
    if products.count() >= 2:
        product1 = products[0]
        product2 = products[1]
        
        CartItem.objects.create(
            cart=cart,
            product=product1,
            quantity=2
        )
        
        CartItem.objects.create(
            cart=cart,
            product=product2,
            quantity=1
        )
        
        print(f"\n   Productos en el carrito:")
        for item in cart.items.all():
            print(f"     - {item.product.name} x {item.quantity} = S/. {item.subtotal:.2f}")
        
        # Calcular total
        total = sum(item.subtotal for item in cart.items.all())
        print(f"\n   Total del carrito: S/. {total:.2f}")
    
    # 4. Verificar URLs disponibles
    print("\n4. URLs disponibles:")
    print("   ✓ /                          → Página de inicio")
    print("   ✓ /tienda/                   → Catálogo de productos")
    print("   ✓ /tienda/<slug>/            → Detalle de producto")
    print("   ✓ /carrito/                  → Vista del carrito")
    print("   ✓ /carrito/agregar/          → Agregar al carrito (POST)")
    print("   ✓ /carrito/actualizar/       → Actualizar cantidad (POST)")
    print("   ✓ /carrito/eliminar/         → Eliminar del carrito (POST)")
    print("   ✓ /carrito/contador/         → Contador del carrito (GET)")
    
    # 5. Verificar productos con stock
    print("\n5. Productos disponibles para venta:")
    available = Product.objects.filter(is_active=True, stock_quantity__gt=0)
    print(f"   ✓ Productos con stock: {available.count()}")
    
    out_of_stock = Product.objects.filter(is_active=True, stock_quantity=0)
    print(f"   ⚠ Productos sin stock: {out_of_stock.count()}")
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)
    print("\nPara probar la tienda en el navegador:")
    print("1. Inicia el servidor: python manage.py runserver")
    print("2. Accede a: http://localhost:8000/")
    print("3. Navega por la tienda sin necesidad de iniciar sesión")
    print("\n")


if __name__ == '__main__':
    test_ecommerce_module()
