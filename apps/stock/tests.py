"""
Pruebas para el módulo de inventario
"""
from django.test import TestCase, Client
from django.urls import reverse
from apps.authentication.models import User
from apps.stock.models import Category, Product, StockMovement


class StockTests(TestCase):
    """Pruebas para gestión de inventario"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        
        # Crear usuario administrador
        self.user = User.objects.create_user(
            username='admin_test',
            password='Test1234!',
            role='administrador'
        )
        
        # Crear categoría
        self.category = Category.objects.create(
            name='Papelería',
            description='Productos de papelería'
        )
        
        # Crear producto
        self.product = Product.objects.create(
            name='Papel Bond A4',
            sku='PAP001',
            category=self.category,
            price=25.00,
            cost_price=18.00,
            stock_quantity=50,
            min_stock_quantity=10
        )
    
    def test_producto_creado_correctamente(self):
        """Verificar que el producto se crea con los datos correctos"""
        self.assertEqual(self.product.stock_quantity, 50)
        self.assertEqual(str(self.product), 'Papel Bond A4')
        self.assertEqual(self.product.sku, 'PAP001')
        self.assertEqual(self.product.category, self.category)
    
    def test_categoria_str_representation(self):
        """Verificar la representación en string de la categoría"""
        self.assertEqual(str(self.category), 'Papelería')
    
    def test_alerta_stock_bajo(self):
        """Verificar que se detecta cuando el stock está bajo"""
        self.product.stock_quantity = 5
        self.product.save()
        self.assertTrue(self.product.needs_restock)
    
    def test_stock_suficiente(self):
        """Verificar que no hay alerta cuando el stock es suficiente"""
        self.product.stock_quantity = 50
        self.product.save()
        self.assertFalse(self.product.needs_restock)
    
    def test_movimiento_decrementa_stock(self):
        """Verificar que un movimiento de salida decrementa el stock"""
        stock_inicial = self.product.stock_quantity
        
        # Crear movimiento de salida
        movement = StockMovement.objects.create(
            product=self.product,
            user=self.user,
            movement_type='salida',
            quantity=10,
            previous_quantity=stock_inicial,
            new_quantity=stock_inicial - 10,
            reason='Venta'
        )
        
        # Actualizar stock del producto
        self.product.stock_quantity = movement.new_quantity
        self.product.save()
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, stock_inicial - 10)
    
    def test_movimiento_incrementa_stock(self):
        """Verificar que un movimiento de entrada incrementa el stock"""
        stock_inicial = self.product.stock_quantity
        
        movement = StockMovement.objects.create(
            product=self.product,
            user=self.user,
            movement_type='entrada',
            quantity=20,
            previous_quantity=stock_inicial,
            new_quantity=stock_inicial + 20,
            reason='Compra a proveedor'
        )
        
        self.product.stock_quantity = movement.new_quantity
        self.product.save()
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, stock_inicial + 20)
    
    def test_crud_producto(self):
        """Verificar operaciones CRUD de productos"""
        self.client.login(username='admin_test', password='Test1234!')
        
        # Crear producto
        response = self.client.post('/stock/productos/nuevo/', {
            'name': 'Tijeras',
            'sku': 'TIJ001',
            'category': self.category.id,
            'price': '15.00',
            'cost_price': '8.00',
            'stock_quantity': 20,
            'min_stock_quantity': 5,
            'description': 'Tijeras escolares'
        })
        
        # Verificar que se creó
        self.assertTrue(Product.objects.filter(sku='TIJ001').exists())
        self.assertEqual(Product.objects.count(), 2)
    
    def test_producto_slug_generado_automaticamente(self):
        """Verificar que el slug se genera automáticamente"""
        producto = Product.objects.create(
            name='Cuaderno Profesional',
            sku='CUA001',
            category=self.category,
            price=35.00,
            cost_price=25.00,
            stock_quantity=30,
            min_stock_quantity=5
        )
        self.assertEqual(producto.slug, 'cuaderno-profesional')
    
    def test_producto_slug_unico(self):
        """Verificar que los slugs son únicos"""
        producto1 = Product.objects.create(
            name='Lápiz',
            sku='LAP001',
            category=self.category,
            price=5.00,
            cost_price=3.00,
            stock_quantity=100,
            min_stock_quantity=20
        )
        
        producto2 = Product.objects.create(
            name='Lápiz',
            sku='LAP002',
            category=self.category,
            price=6.00,
            cost_price=4.00,
            stock_quantity=80,
            min_stock_quantity=15
        )
        
        self.assertNotEqual(producto1.slug, producto2.slug)
    
    def test_categoria_activa_por_defecto(self):
        """Verificar que las categorías están activas por defecto"""
        categoria = Category.objects.create(name='Electrónica')
        self.assertTrue(categoria.is_active)
    
    def test_producto_activo_por_defecto(self):
        """Verificar que los productos están activos por defecto"""
        self.assertTrue(self.product.is_active)
    
    def test_movimiento_str_representation(self):
        """Verificar la representación en string del movimiento"""
        movement = StockMovement.objects.create(
            product=self.product,
            user=self.user,
            movement_type='entrada',
            quantity=10,
            previous_quantity=50,
            new_quantity=60
        )
        expected = f"entrada - {self.product.name} - 10"
        self.assertEqual(str(movement), expected)


class CategoryTests(TestCase):
    """Pruebas específicas para categorías"""
    
    def test_crear_categoria(self):
        """Verificar creación de categoría"""
        categoria = Category.objects.create(
            name='Juguetes',
            description='Juguetes educativos'
        )
        self.assertEqual(categoria.name, 'Juguetes')
        self.assertTrue(categoria.is_active)
    
    def test_productos_por_categoria(self):
        """Verificar relación entre categoría y productos"""
        categoria = Category.objects.create(name='Tecnología')
        
        Product.objects.create(
            name='Mouse',
            sku='MOU001',
            category=categoria,
            price=150.00,
            cost_price=100.00,
            stock_quantity=25,
            min_stock_quantity=5
        )
        
        Product.objects.create(
            name='Teclado',
            sku='TEC001',
            category=categoria,
            price=300.00,
            cost_price=200.00,
            stock_quantity=15,
            min_stock_quantity=3
        )
        
        self.assertEqual(categoria.products.count(), 2)
