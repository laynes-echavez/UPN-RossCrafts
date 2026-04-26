"""
Pruebas para el módulo de autenticación
"""
from django.test import TestCase, Client
from django.urls import reverse
from apps.authentication.models import User


class AuthenticationTests(TestCase):
    """Pruebas para autenticación y autorización"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        
        # Crear usuarios de prueba
        self.gerente = User.objects.create_user(
            username='gerente_test',
            password='Test1234!',
            role='gerente',
            email='gerente@test.com'
        )
        
        self.empleado = User.objects.create_user(
            username='empleado_test',
            password='Test1234!',
            role='empleado',
            email='empleado@test.com'
        )
        
        self.administrador = User.objects.create_user(
            username='admin_test',
            password='Test1234!',
            role='administrador',
            email='admin@test.com'
        )
    
    def test_login_exitoso_gerente(self):
        """Verificar que un gerente puede iniciar sesión correctamente"""
        response = self.client.post('/auth/login/', {
            'username': 'gerente_test',
            'password': 'Test1234!'
        })
        self.assertEqual(response.status_code, 302)  # Redirige
        self.assertTrue(response.url.startswith('/auth/dashboard'))
    
    def test_login_exitoso_empleado(self):
        """Verificar que un empleado puede iniciar sesión correctamente"""
        response = self.client.post('/auth/login/', {
            'username': 'empleado_test',
            'password': 'Test1234!'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_login_credenciales_incorrectas(self):
        """Verificar que credenciales incorrectas son rechazadas"""
        response = self.client.post('/auth/login/', {
            'username': 'gerente_test',
            'password': 'WRONG_PASSWORD'
        })
        self.assertEqual(response.status_code, 200)  # No redirige
        self.assertContains(response, 'credenciales', status_code=200)
    
    def test_login_usuario_inexistente(self):
        """Verificar que usuarios inexistentes no pueden iniciar sesión"""
        response = self.client.post('/auth/login/', {
            'username': 'usuario_inexistente',
            'password': 'Test1234!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'credenciales', status_code=200)
    
    def test_empleado_no_accede_a_vista_gerente(self):
        """Verificar que empleados no pueden acceder a vistas de gerente"""
        self.client.login(username='empleado_test', password='Test1234!')
        response = self.client.get('/auth/dashboard/auditoria/')
        self.assertIn(response.status_code, [302, 403])
    
    def test_gerente_accede_a_auditoria(self):
        """Verificar que gerentes pueden acceder a auditoría"""
        self.client.login(username='gerente_test', password='Test1234!')
        response = self.client.get('/auth/dashboard/auditoria/')
        self.assertIn(response.status_code, [200, 302])
    
    def test_logout_cierra_sesion(self):
        """Verificar que el logout cierra la sesión correctamente"""
        self.client.login(username='gerente_test', password='Test1234!')
        self.client.get('/auth/logout/')
        
        # Intentar acceder a dashboard sin sesión
        response = self.client.get('/auth/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirige a login
        self.assertTrue(response.url.startswith('/auth/login'))
    
    def test_usuario_sin_autenticar_redirige_a_login(self):
        """Verificar que usuarios no autenticados son redirigidos al login"""
        response = self.client.get('/auth/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/auth/login'))
    
    def test_creacion_usuario_con_rol(self):
        """Verificar que se pueden crear usuarios con roles específicos"""
        nuevo_usuario = User.objects.create_user(
            username='nuevo_test',
            password='Test1234!',
            role='empleado'
        )
        self.assertEqual(nuevo_usuario.role, 'empleado')
        self.assertTrue(nuevo_usuario.check_password('Test1234!'))
    
    def test_usuario_str_representation(self):
        """Verificar la representación en string del usuario"""
        self.assertEqual(str(self.gerente), 'gerente_test')


class UserModelTests(TestCase):
    """Pruebas para el modelo User"""
    
    def test_crear_usuario_basico(self):
        """Verificar creación de usuario básico"""
        user = User.objects.create_user(
            username='test_user',
            password='Test1234!',
            email='test@test.com'
        )
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.role, 'empleado')  # Rol por defecto
        self.assertTrue(user.is_active)
    
    def test_roles_disponibles(self):
        """Verificar que todos los roles están disponibles"""
        roles = ['gerente', 'administrador', 'empleado']
        for role in roles:
            user = User.objects.create_user(
                username=f'user_{role}',
                password='Test1234!',
                role=role
            )
            self.assertEqual(user.role, role)
    
    def test_usuario_con_telefono(self):
        """Verificar que se puede agregar teléfono al usuario"""
        user = User.objects.create_user(
            username='user_phone',
            password='Test1234!',
            phone='5551234567'
        )
        self.assertEqual(user.phone, '5551234567')
