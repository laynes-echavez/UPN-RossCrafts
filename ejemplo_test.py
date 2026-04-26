"""
Ejemplo de cómo escribir tests en Django
Este archivo es solo para referencia y aprendizaje
"""
from django.test import TestCase, Client
from django.urls import reverse
from apps.authentication.models import User
from apps.stock.models import Category, Product
from decimal import Decimal


class EjemploTestBasico(TestCase):
    """
    Ejemplo básico de test en Django
    """
    
    def setUp(self):
        """
        setUp() se ejecuta ANTES de cada método test_*
        Úsalo para crear datos que necesitas en tus tests
        """
        # Crear un cliente HTTP para hacer requests
        self.client = Client()
        
        # Crear un usuario de prueba
        self.user = User.objects.create_user(
            username='test_user',
            password='Test1234!',
            role='empleado'
        )
        
        # Crear datos de prueba
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST001',
            category=self.category,
            price=Decimal('100.00'),
            cost_price=Decimal('50.00'),
            stock_quantity=10,
            min_stock_quantity=5
        )
    
    def test_ejemplo_assertion_basico(self):
        """
        Ejemplo de assertions básicos
        """
        # assertEqual - verifica que dos valores sean iguales
        self.assertEqual(1 + 1, 2)
        self.assertEqual(self.product.name, 'Test Product')
        
        # assertTrue / assertFalse
        self.assertTrue(True)
        self.assertFalse(False)
        self.assertTrue(self.product.stock_quantity > 0)
        
        # assertIn / assertNotIn
        self.assertIn('Test', self.product.name)
        self.assertNotIn('XYZ', self.product.name)
        
        # assertIsNone / assertIsNotNone
        self.assertIsNotNone(self.product)
        
        # assertGreater / assertLess
        self.assertGreater(self.product.price, Decimal('0'))
        self.assertLess(self.product.cost_price, self.product.price)
    
    def test_ejemplo_request_get(self):
        """
        Ejemplo de hacer un request GET
        """
        # Login primero
        self.client.login(username='test_user', password='Test1234!')
        
        # Hacer request GET
        response = self.client.get('/stock/productos/')
        
        # Verificar status code
        self.assertEqual(response.status_code, 200)
        
        # Verificar contenido
        self.assertContains(response, 'Test Product')
        
        # Verificar contexto (variables pasadas al template)
        self.assertIn('products', response.context)
    
    def test_ejemplo_request_post(self):
        """
        Ejemplo de hacer un request POST
        """
        self.client.login(username='test_user', password='Test1234!')
        
        # Datos para enviar
        data = {
            'name': 'New Product',
            'sku': 'NEW001',
            'category': self.category.id,
            'price': '150.00',
            'cost_price': '75.00',
            'stock_quantity': 20,
            'min_stock_quantity': 5
        }
        
        # Hacer request POST
        response = self.client.post('/stock/productos/nuevo/', data)
        
        # Verificar redirección (302)
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se creó el producto
        self.assertTrue(Product.objects.filter(sku='NEW001').exists())
    
    def test_ejemplo_request_json(self):
        """
        Ejemplo de request con JSON
        """
        import json
        
        self.client.login(username='test_user', password='Test1234!')
        
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        
        response = self.client.post(
            '/carrito/agregar/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Parsear respuesta JSON
        response_data = json.loads(response.content)
        
        # Verificar datos
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response_data)
    
    def test_ejemplo_verificar_base_datos(self):
        """
        Ejemplo de verificar cambios en la base de datos
        """
        # Contar productos antes
        count_before = Product.objects.count()
        
        # Crear nuevo producto
        Product.objects.create(
            name='Another Product',
            sku='ANO001',
            category=self.category,
            price=Decimal('200.00'),
            cost_price=Decimal('100.00'),
            stock_quantity=15,
            min_stock_quantity=5
        )
        
        # Verificar que aumentó el conteo
        count_after = Product.objects.count()
        self.assertEqual(count_after, count_before + 1)
        
        # Verificar que existe
        self.assertTrue(Product.objects.filter(sku='ANO001').exists())
        
        # Obtener y verificar
        product = Product.objects.get(sku='ANO001')
        self.assertEqual(product.name, 'Another Product')
    
    def test_ejemplo_actualizar_objeto(self):
        """
        Ejemplo de actualizar un objeto
        """
        # Cambiar precio
        self.product.price = Decimal('120.00')
        self.product.save()
        
        # Refrescar desde BD
        self.product.refresh_from_db()
        
        # Verificar cambio
        self.assertEqual(self.product.price, Decimal('120.00'))
    
    def test_ejemplo_eliminar_objeto(self):
        """
        Ejemplo de eliminar un objeto
        """
        product_id = self.product.id
        
        # Eliminar
        self.product.delete()
        
        # Verificar que no existe
        self.assertFalse(Product.objects.filter(id=product_id).exists())
    
    def test_ejemplo_excepciones(self):
        """
        Ejemplo de verificar que se lanzan excepciones
        """
        # Verificar que se lanza ValueError
        with self.assertRaises(ValueError):
            raise ValueError("Error de prueba")
        
        # Verificar que NO se lanza excepción
        try:
            x = 1 + 1
        except Exception:
            self.fail("No debería lanzar excepción")
    
    def test_ejemplo_permisos(self):
        """
        Ejemplo de verificar permisos de acceso
        """
        # Sin login - debe redirigir
        response = self.client.get('/auth/dashboard/')
        self.assertEqual(response.status_code, 302)
        
        # Con login - debe permitir
        self.client.login(username='test_user', password='Test1234!')
        response = self.client.get('/auth/dashboard/')
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        """
        tearDown() se ejecuta DESPUÉS de cada método test_*
        Úsalo para limpiar recursos (opcional, Django lo hace automáticamente)
        """
        pass


class EjemploTestConMocking(TestCase):
    """
    Ejemplo de tests con mocking (simular servicios externos)
    """
    
    def setUp(self):
        self.client = Client()
    
    def test_ejemplo_mock_stripe(self):
        """
        Ejemplo de mockear Stripe
        """
        from unittest.mock import patch, MagicMock
        
        # Mockear la función de Stripe
        with patch('stripe.PaymentIntent.create') as mock_create:
            # Configurar qué debe retornar el mock
            mock_create.return_value = MagicMock(
                id='pi_test123',
                client_secret='secret_test',
                status='succeeded'
            )
            
            # Llamar a tu código que usa Stripe
            # (aquí simularíamos la llamada)
            result = mock_create(amount=1000, currency='mxn')
            
            # Verificar que se llamó
            mock_create.assert_called_once()
            
            # Verificar el resultado
            self.assertEqual(result.id, 'pi_test123')
    
    def test_ejemplo_mock_email(self):
        """
        Ejemplo de mockear envío de emails
        """
        from django.core import mail
        
        # Enviar email (en tests usa backend en memoria)
        mail.send_mail(
            'Subject',
            'Message',
            'from@example.com',
            ['to@example.com'],
        )
        
        # Verificar que se envió
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject')


class EjemploTestAvanzado(TestCase):
    """
    Ejemplos de tests más avanzados
    """
    
    def test_ejemplo_multiples_assertions(self):
        """
        Ejemplo con múltiples verificaciones
        """
        user = User.objects.create_user(
            username='advanced_user',
            password='Test1234!',
            email='test@example.com',
            role='gerente'
        )
        
        # Verificar múltiples propiedades
        self.assertEqual(user.username, 'advanced_user')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'gerente')
        self.assertTrue(user.check_password('Test1234!'))
        self.assertTrue(user.is_active)
    
    def test_ejemplo_subtest(self):
        """
        Ejemplo de subtests (para probar múltiples casos)
        """
        test_cases = [
            ('empleado', '/auth/dashboard/'),
            ('gerente', '/auth/dashboard/auditoria/'),
            ('administrador', '/stock/productos/'),
        ]
        
        for role, url in test_cases:
            with self.subTest(role=role, url=url):
                user = User.objects.create_user(
                    username=f'user_{role}',
                    password='Test1234!',
                    role=role
                )
                self.client.login(username=f'user_{role}', password='Test1234!')
                response = self.client.get(url)
                self.assertIn(response.status_code, [200, 302])


# NOTAS IMPORTANTES:
# 
# 1. Cada clase debe heredar de TestCase
# 2. Cada método de test debe empezar con "test_"
# 3. setUp() se ejecuta antes de cada test
# 4. tearDown() se ejecuta después de cada test (opcional)
# 5. Los tests deben ser independientes
# 6. Usa nombres descriptivos
# 7. Un test debe verificar una sola cosa
# 8. Los datos se crean y destruyen automáticamente
# 
# Para ejecutar este ejemplo:
# python manage.py test --settings=settings.test ejemplo_test
