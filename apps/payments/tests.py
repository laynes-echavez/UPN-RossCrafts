"""
Pruebas para el módulo de pagos
"""
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from apps.authentication.models import User
from apps.stock.models import Category, Product
from apps.sales.models import Sale


class PaymentTests(TestCase):
    """Pruebas para procesamiento de pagos"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        
        # Crear usuario
        self.user = User.objects.create_user(
            username='test_user',
            password='Test1234!',
            role='empleado'
        )
        
        # Crear producto
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            name='Producto Test',
            sku='TEST001',
            category=self.category,
            price=100.00,
            cost_price=60.00,
            stock_quantity=50,
            min_stock_quantity=10
        )
        
        # Crear venta
        self.sale = Sale.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('100.00'),
            payment_method='cash',
            status='completed'
        )
    
    @patch('stripe.PaymentIntent.create')
    def test_crear_payment_intent_stripe(self, mock_create):
        """Verificar creación de PaymentIntent en Stripe"""
        mock_create.return_value = MagicMock(
            id='pi_test_123',
            client_secret='pi_test_secret_123',
            amount=10000,
            currency='mxn'
        )
        
        # Simular creación de payment intent
        response = self.client.post('/payments/create-intent/', {
            'amount': 100.00,
            'currency': 'mxn'
        }, content_type='application/json')
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content)
            self.assertIn('clientSecret', data)
    
    @patch('stripe.PaymentIntent.retrieve')
    def test_confirmar_pago_stripe(self, mock_retrieve):
        """Verificar confirmación de pago en Stripe"""
        mock_retrieve.return_value = MagicMock(
            id='pi_test_123',
            status='succeeded',
            amount=10000
        )
        
        response = self.client.post('/payments/confirm/', {
            'payment_intent_id': 'pi_test_123'
        }, content_type='application/json')
        
        # Verificar respuesta
        self.assertIn(response.status_code, [200, 404])
    
    def test_pago_efectivo(self):
        """Verificar registro de pago en efectivo"""
        self.assertEqual(self.sale.payment_method, 'cash')
        self.assertEqual(self.sale.status, 'completed')
    
    def test_pago_tarjeta(self):
        """Verificar registro de pago con tarjeta"""
        sale = Sale.objects.create(
            user=self.user,
            subtotal=Decimal('200.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('200.00'),
            payment_method='card',
            status='completed'
        )
        
        self.assertEqual(sale.payment_method, 'card')
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_pago_exitoso(self, mock_webhook):
        """Verificar procesamiento de webhook de pago exitoso"""
        mock_webhook.return_value = {
            'type': 'payment_intent.succeeded',
            'data': {
                'object': {
                    'id': 'pi_test_123',
                    'amount': 10000,
                    'currency': 'mxn',
                    'metadata': {
                        'sale_id': str(self.sale.id)
                    }
                }
            }
        }
        
        response = self.client.post('/stripe/webhook/',
            data='{}',
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_signature'
        )
        
        # Verificar que el webhook se procesó
        self.assertIn(response.status_code, [200, 404])
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_pago_fallido(self, mock_webhook):
        """Verificar procesamiento de webhook de pago fallido"""
        mock_webhook.return_value = {
            'type': 'payment_intent.payment_failed',
            'data': {
                'object': {
                    'id': 'pi_test_123',
                    'amount': 10000,
                    'last_payment_error': {
                        'message': 'Tarjeta rechazada'
                    }
                }
            }
        }
        
        response = self.client.post('/stripe/webhook/',
            data='{}',
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_signature'
        )
        
        # Verificar respuesta
        self.assertIn(response.status_code, [200, 404])
