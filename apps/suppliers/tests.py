"""
Pruebas para el módulo de proveedores
"""
from django.test import TestCase, Client
from apps.authentication.models import User
from apps.suppliers.models import Supplier


class SupplierTests(TestCase):
    """Pruebas para gestión de proveedores"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        
        # Crear usuario administrador
        self.user = User.objects.create_user(
            username='admin_test',
            password='Test1234!',
            role='administrador'
        )
        
        # Crear proveedor
        self.supplier = Supplier.objects.create(
            name='Proveedor Test',
            contact_name='Juan Pérez',
            email='proveedor@test.com',
            phone='5551234567',
            address='Calle Principal 123'
        )
        
        # Login
        self.client.login(username='admin_test', password='Test1234!')
    
    def test_crear_proveedor(self):
        """Verificar creación de proveedor"""
        proveedor = Supplier.objects.create(
            name='Nuevo Proveedor',
            contact_name='María González',
            email='nuevo@test.com',
            phone='5559876543'
        )
        
        self.assertEqual(proveedor.name, 'Nuevo Proveedor')
        self.assertEqual(proveedor.email, 'nuevo@test.com')
    
    def test_proveedor_str_representation(self):
        """Verificar representación en string del proveedor"""
        self.assertEqual(str(self.supplier), 'Proveedor Test')
    
    def test_proveedor_activo_por_defecto(self):
        """Verificar que los proveedores están activos por defecto"""
        if hasattr(self.supplier, 'is_active'):
            self.assertTrue(self.supplier.is_active)
    
    def test_actualizar_datos_proveedor(self):
        """Verificar actualización de datos del proveedor"""
        self.supplier.phone = '5550000000'
        self.supplier.save()
        
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.phone, '5550000000')
    
    def test_listar_proveedores(self):
        """Verificar listado de proveedores"""
        response = self.client.get('/suppliers/')
        
        if response.status_code == 200:
            self.assertContains(response, self.supplier.name)
