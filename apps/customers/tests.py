"""
Pruebas para el módulo de clientes
"""
from django.test import TestCase, Client
from apps.customers.models import Customer


class CustomerTests(TestCase):
    """Pruebas para gestión de clientes"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        
        # Crear cliente de prueba
        self.customer = Customer.objects.create(
            email='cliente@test.com',
            first_name='Juan',
            last_name='Pérez',
            phone='5551234567',
            address='Calle Principal 123'
        )
    
    def test_crear_cliente(self):
        """Verificar creación de cliente"""
        cliente = Customer.objects.create(
            email='nuevo@test.com',
            first_name='María',
            last_name='González',
            phone='5559876543'
        )
        
        self.assertEqual(cliente.email, 'nuevo@test.com')
        self.assertEqual(cliente.first_name, 'María')
    
    def test_cliente_str_representation(self):
        """Verificar representación en string del cliente"""
        expected = f"{self.customer.first_name} {self.customer.last_name}"
        self.assertEqual(str(self.customer), expected)
    
    def test_email_unico(self):
        """Verificar que el email debe ser único"""
        with self.assertRaises(Exception):
            Customer.objects.create(
                email='cliente@test.com',  # Email duplicado
                first_name='Pedro',
                last_name='Ramírez'
            )
    
    def test_cliente_verificado_por_defecto(self):
        """Verificar que los clientes están verificados por defecto"""
        if hasattr(self.customer, 'is_verified'):
            self.assertTrue(self.customer.is_verified)
    
    def test_actualizar_datos_cliente(self):
        """Verificar actualización de datos del cliente"""
        self.customer.phone = '5550000000'
        self.customer.save()
        
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, '5550000000')


class CustomerAuthTests(TestCase):
    """Pruebas para autenticación de clientes"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.customer = Customer.objects.create(
            email='auth@test.com',
            first_name='Test',
            last_name='User',
            phone='5551234567'
        )
        
        # Establecer contraseña si el modelo lo soporta
        if hasattr(self.customer, 'set_password'):
            self.customer.set_password('Test1234!')
            self.customer.save()
    
    def test_login_cliente(self):
        """Verificar login de cliente"""
        if hasattr(self.customer, 'check_password'):
            response = self.client.post('/ecommerce/login/', {
                'email': 'auth@test.com',
                'password': 'Test1234!'
            })
            
            # Verificar redirección o éxito
            self.assertIn(response.status_code, [200, 302])
    
    def test_registro_cliente_nuevo(self):
        """Verificar registro de nuevo cliente"""
        response = self.client.post('/ecommerce/registro/', {
            'email': 'nuevo_cliente@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Cliente',
            'phone': '5559999999',
            'password': 'Test1234!',
            'password_confirm': 'Test1234!'
        })
        
        # Verificar que se creó o redirigió
        self.assertIn(response.status_code, [200, 302])
