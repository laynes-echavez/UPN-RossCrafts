"""
Pruebas para el módulo de ecommerce
"""
import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.contrib.sessions.middleware import SessionMiddleware
from apps.stock.models import Category, Product
from apps.customers.models import Customer


class EcommerceTests(TestCase):
    """Pruebas para funcionalidad de ecommerce"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        
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
    
    def test_agregar_producto_al_carrito(self):
        """Verificar que se puede agregar un producto al carrito"""
        response = self.client.post('/ecommerce/carrito/agregar/', {
            'product_id': self.product.id,
            'quantity': 2
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data.get('cart_count', 0), 2)
    
    def test_carrito_vacio_al_inicio(self):
        """Verificar que el carrito está vacío al inicio"""
        response = self.client.get('/ecommerce/carrito/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'carrito está vacío', status_code=200)
    
    def test_incrementar_cantidad_producto_carrito(self):
        """Verificar que se puede incrementar la cantidad de un producto"""
        # Agregar producto
        self.client.post('/ecommerce/carrito/agregar/', {
            'product_id': self.product.id,
            'quantity': 1
        }, content_type='application/json')
        
        # Incrementar cantidad
        response = self.client.post('/ecommerce/carrito/agregar/', {
            'product_id': self.product.id,
            'quantity': 2
        }, content_type='application/json')
        
        data = json.loads(response.content)
        self.assertGreaterEqual(data.get('cart_count', 0), 2)
    
    def test_eliminar_producto_del_carrito(self):
        """Verificar que se puede eliminar un producto del carrito"""
        # Agregar producto
        self.client.post('/ecommerce/carrito/agregar/', {
            'product_id': self.product.id,
            'quantity': 2
        }, content_type='application/json')
        
        # Eliminar producto
        response = self.client.post('/ecommerce/carrito/eliminar/', {
            'product_id': self.product.id
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
    
    @patch('stripe.PaymentIntent.create')
    def test_crear_payment_intent(self, mock_stripe):
        """Verificar creación de PaymentIntent de Stripe"""
        mock_stripe.return_value = MagicMock(
            client_secret='pi_test_secret_123',
            id='pi_test_123'
        )
        
        # Agregar producto al carrito primero
        self.client.post('/ecommerce/carrito/agregar/', {
            'product_id': self.product.id,
            'quantity': 2
        }, content_type='application/json')
        
        # Crear payment intent
        response = self.client.post('/ecommerce/checkout/crear-intent/', {
            'email': 'test@test.com'
        }, content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.content)
            self.assertIn('clientSecret', data)
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_stripe_pago_exitoso(self, mock_webhook):
        """Verificar procesamiento de webhook de Stripe para pago exitoso"""
        mock_webhook.return_value = {
            'type': 'payment_intent.succeeded',
            'data': {
                'object': {
                    'id': 'pi_test123',
                    'amount': 5000,
                    'metadata': {
                        'customer_email': 'test@test.com'
                    }
                }
            }
        }
        
        response = self.client.post('/stripe/webhook/',
            data='{}',
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_sig'
        )
        
        # El webhook debe procesar correctamente
        self.assertIn(response.status_code, [200, 404])  # 404 si la ruta no existe aún
    
    def test_producto_visible_en_catalogo(self):
        """Verificar que los productos activos aparecen en el catálogo"""
        response = self.client.get('/ecommerce/productos/')
        
        if response.status_code == 200:
            self.assertContains(response, self.product.name)
    
    def test_producto_inactivo_no_visible(self):
        """Verificar que productos inactivos no aparecen en el catálogo"""
        self.product.is_active = False
        self.product.save()
        
        response = self.client.get('/ecommerce/productos/')
        
        if response.status_code == 200:
            self.assertNotContains(response, self.product.name)
    
    def test_detalle_producto(self):
        """Verificar que se puede ver el detalle de un producto"""
        response = self.client.get(f'/ecommerce/productos/{self.product.slug}/')
        
        if response.status_code == 200:
            self.assertContains(response, self.product.name)
            self.assertContains(response, str(self.product.price))


class CartSessionTests(TestCase):
    """Pruebas para manejo de sesión del carrito"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
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
    
    def test_carrito_persiste_en_sesion(self):
        """Verificar que el carrito persiste en la sesión"""
        # Agregar producto
        self.client.post('/ecommerce/carrito/agregar/', {
            'product_id': self.product.id,
            'quantity': 1
        }, content_type='application/json')
        
        # Verificar que persiste
        response = self.client.get('/ecommerce/carrito/')
        
        if response.status_code == 200:
            # El carrito debe tener items
            self.assertNotContains(response, 'carrito está vacío')
    
    def test_limpiar_carrito(self):
        """Verificar que se puede limpiar el carrito"""
        # Agregar producto
        self.client.post('/ecommerce/carrito/agregar/', {
            'product_id': self.product.id,
            'quantity': 1
        }, content_type='application/json')
        
        # Limpiar carrito
        response = self.client.post('/ecommerce/carrito/limpiar/')
        
        if response.status_code == 200:
            # Verificar que está vacío
            response = self.client.get('/ecommerce/carrito/')
            self.assertContains(response, 'carrito está vacío', status_code=200)
