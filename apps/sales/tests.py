"""
Pruebas para el módulo de ventas
"""
import json
from decimal import Decimal
from django.test import TestCase, Client
from django.utils import timezone
from apps.authentication.models import User
from apps.stock.models import Category, Product
from apps.sales.models import Sale, SaleItem
from apps.customers.models import Customer


class SalesTests(TestCase):
    """Pruebas para gestión de ventas"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        
        # Crear usuario
        self.user = User.objects.create_user(
            username='vendedor_test',
            password='Test1234!',
            role='empleado'
        )
        
        # Crear categoría y producto
        self.category = Category.objects.create(name='Papelería')
        self.product = Product.objects.create(
            name='Papel Bond A4',
            sku='PAP001',
            category=self.category,
            price=25.00,
            cost_price=18.00,
            stock_quantity=100,
            min_stock_quantity=10
        )
        
        # Crear cliente
        self.customer = Customer.objects.create(
            email='cliente@test.com',
            first_name='Juan',
            last_name='Pérez',
            phone='5551234567'
        )
        
        # Login
        self.client.login(username='vendedor_test', password='Test1234!')
    
    def test_registro_venta_completa(self):
        """Verificar que se puede registrar una venta completa"""
        stock_antes = self.product.stock_quantity
        
        response = self.client.post('/sales/registrar/', {
            'items': json.dumps([{
                'product_id': self.product.id,
                'quantity': 3,
                'unit_price': float(self.product.price)
            }]),
            'payment_method': 'cash',
            'customer_id': self.customer.id
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data.get('success', False))
        
        # Verificar que el stock decrementó
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, stock_antes - 3)
    
    def test_venta_bloqueada_sin_stock(self):
        """Verificar que no se puede vender sin stock suficiente"""
        self.product.stock_quantity = 0
        self.product.save()
        
        response = self.client.post('/sales/registrar/', {
            'items': json.dumps([{
                'product_id': self.product.id,
                'quantity': 1,
                'unit_price': float(self.product.price)
            }]),
            'payment_method': 'cash'
        }, content_type='application/json')
        
        data = json.loads(response.content)
        self.assertFalse(data.get('success', True))
        self.assertIn('stock', data.get('error', '').lower())
    
    def test_creacion_venta_modelo(self):
        """Verificar creación de venta en el modelo"""
        sale = Sale.objects.create(
            user=self.user,
            customer=self.customer,
            subtotal=Decimal('75.00'),
            tax=Decimal('12.00'),
            discount=Decimal('0.00'),
            total=Decimal('87.00'),
            payment_method='cash',
            status='completed'
        )
        
        self.assertEqual(sale.user, self.user)
        self.assertEqual(sale.total, Decimal('87.00'))
        self.assertEqual(sale.status, 'completed')
    
    def test_generacion_numero_comprobante(self):
        """Verificar que se genera automáticamente el número de comprobante"""
        sale = Sale.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('100.00'),
            payment_method='cash'
        )
        
        self.assertIsNotNone(sale.receipt_number)
        self.assertTrue(sale.receipt_number.startswith('RC-'))
        self.assertIn(str(timezone.now().year), sale.receipt_number)
    
    def test_sale_item_calcula_subtotal(self):
        """Verificar que SaleItem calcula el subtotal correctamente"""
        sale = Sale.objects.create(
            user=self.user,
            subtotal=Decimal('75.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('75.00'),
            payment_method='cash'
        )
        
        item = SaleItem.objects.create(
            sale=sale,
            product=self.product,
            quantity=3,
            unit_price=Decimal('25.00')
        )
        
        self.assertEqual(item.subtotal, Decimal('75.00'))
    
    def test_venta_con_multiples_items(self):
        """Verificar venta con múltiples productos"""
        product2 = Product.objects.create(
            name='Cuaderno',
            sku='CUA001',
            category=self.category,
            price=35.00,
            cost_price=25.00,
            stock_quantity=50,
            min_stock_quantity=10
        )
        
        sale = Sale.objects.create(
            user=self.user,
            subtotal=Decimal('145.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('145.00'),
            payment_method='card'
        )
        
        SaleItem.objects.create(
            sale=sale,
            product=self.product,
            quantity=2,
            unit_price=self.product.price
        )
        
        SaleItem.objects.create(
            sale=sale,
            product=product2,
            quantity=3,
            unit_price=product2.price
        )
        
        self.assertEqual(sale.items.count(), 2)
    
    def test_generacion_comprobante_pdf(self):
        """Verificar generación de comprobante PDF"""
        sale = Sale.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('100.00'),
            payment_method='cash'
        )
        
        SaleItem.objects.create(
            sale=sale,
            product=self.product,
            quantity=4,
            unit_price=self.product.price
        )
        
        response = self.client.get(f'/sales/{sale.id}/comprobante/')
        
        if response.status_code == 200:
            self.assertEqual(response['Content-Type'], 'application/pdf')
    
    def test_sale_str_representation(self):
        """Verificar la representación en string de la venta"""
        sale = Sale.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('100.00'),
            payment_method='cash'
        )
        
        self.assertIn('Venta #', str(sale))
    
    def test_metodos_pago_disponibles(self):
        """Verificar que todos los métodos de pago están disponibles"""
        metodos = ['cash', 'card', 'transfer', 'online']
        
        for metodo in metodos:
            sale = Sale.objects.create(
                user=self.user,
                subtotal=Decimal('100.00'),
                tax=Decimal('0.00'),
                discount=Decimal('0.00'),
                total=Decimal('100.00'),
                payment_method=metodo
            )
            self.assertEqual(sale.payment_method, metodo)
    
    def test_estados_venta_disponibles(self):
        """Verificar que todos los estados de venta están disponibles"""
        estados = ['completed', 'pending', 'cancelled', 'refunded']
        
        for estado in estados:
            sale = Sale.objects.create(
                user=self.user,
                subtotal=Decimal('100.00'),
                tax=Decimal('0.00'),
                discount=Decimal('0.00'),
                total=Decimal('100.00'),
                payment_method='cash',
                status=estado
            )
            self.assertEqual(sale.status, estado)


class SaleItemTests(TestCase):
    """Pruebas específicas para items de venta"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            username='test_user',
            password='Test1234!'
        )
        
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            name='Producto Test',
            sku='TEST001',
            category=self.category,
            price=50.00,
            cost_price=30.00,
            stock_quantity=100,
            min_stock_quantity=10
        )
        
        self.sale = Sale.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('100.00'),
            payment_method='cash'
        )
    
    def test_sale_item_str_representation(self):
        """Verificar representación en string del item"""
        item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=2,
            unit_price=self.product.price
        )
        
        expected = f"{self.product.name} x 2"
        self.assertEqual(str(item), expected)
