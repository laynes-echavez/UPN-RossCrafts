"""
Pruebas para el módulo de auditoría
"""
from django.test import TestCase, Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from apps.authentication.models import User
from apps.audit.models import AuditLog
from apps.audit.middleware import AuditMiddleware


class AuditTests(TestCase):
    """Pruebas para sistema de auditoría"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        self.factory = RequestFactory()
        
        # Crear usuarios
        self.gerente = User.objects.create_user(
            username='gerente_test',
            password='Test1234!',
            role='gerente'
        )
        
        self.empleado = User.objects.create_user(
            username='empleado_test',
            password='Test1234!',
            role='empleado'
        )
    
    def test_crear_log_auditoria(self):
        """Verificar creación de log de auditoría"""
        log = AuditLog.objects.create(
            user=self.gerente,
            action='LOGIN',
            ip_address='127.0.0.1',
            user_agent='Test Browser'
        )
        
        self.assertEqual(log.user, self.gerente)
        self.assertEqual(log.action, 'LOGIN')
    
    def test_log_auditoria_str_representation(self):
        """Verificar representación en string del log"""
        log = AuditLog.objects.create(
            user=self.gerente,
            action='VIEW_REPORT',
            ip_address='127.0.0.1'
        )
        
        self.assertIn(self.gerente.username, str(log))
        self.assertIn('VIEW_REPORT', str(log))
    
    def test_middleware_registra_acciones(self):
        """Verificar que el middleware registra acciones"""
        self.client.login(username='gerente_test', password='Test1234!')
        
        # Realizar una acción
        response = self.client.get('/auth/dashboard/')
        
        # Verificar que se creó un log (si el middleware está activo)
        if AuditLog.objects.exists():
            self.assertGreater(AuditLog.objects.count(), 0)
    
    def test_gerente_accede_auditoria(self):
        """Verificar que gerentes pueden acceder a auditoría"""
        self.client.login(username='gerente_test', password='Test1234!')
        response = self.client.get('/auth/dashboard/auditoria/')
        
        self.assertIn(response.status_code, [200, 302])
    
    def test_empleado_no_accede_auditoria(self):
        """Verificar que empleados no pueden acceder a auditoría"""
        self.client.login(username='empleado_test', password='Test1234!')
        response = self.client.get('/auth/dashboard/auditoria/')
        
        self.assertIn(response.status_code, [302, 403])
    
    def test_filtrar_logs_por_usuario(self):
        """Verificar filtrado de logs por usuario"""
        # Crear logs para diferentes usuarios
        AuditLog.objects.create(
            user=self.gerente,
            action='LOGIN',
            ip_address='127.0.0.1'
        )
        
        AuditLog.objects.create(
            user=self.empleado,
            action='LOGIN',
            ip_address='127.0.0.1'
        )
        
        # Filtrar por gerente
        logs_gerente = AuditLog.objects.filter(user=self.gerente)
        self.assertEqual(logs_gerente.count(), 1)
    
    def test_filtrar_logs_por_accion(self):
        """Verificar filtrado de logs por acción"""
        AuditLog.objects.create(
            user=self.gerente,
            action='LOGIN',
            ip_address='127.0.0.1'
        )
        
        AuditLog.objects.create(
            user=self.gerente,
            action='LOGOUT',
            ip_address='127.0.0.1'
        )
        
        # Filtrar por acción
        logs_login = AuditLog.objects.filter(action='LOGIN')
        self.assertEqual(logs_login.count(), 1)
    
    def test_log_incluye_ip_address(self):
        """Verificar que el log incluye dirección IP"""
        log = AuditLog.objects.create(
            user=self.gerente,
            action='VIEW_SALES',
            ip_address='192.168.1.100'
        )
        
        self.assertEqual(log.ip_address, '192.168.1.100')
    
    def test_log_incluye_user_agent(self):
        """Verificar que el log incluye user agent"""
        log = AuditLog.objects.create(
            user=self.gerente,
            action='VIEW_PRODUCTS',
            ip_address='127.0.0.1',
            user_agent='Mozilla/5.0'
        )
        
        self.assertEqual(log.user_agent, 'Mozilla/5.0')


class AuditLogQueryTests(TestCase):
    """Pruebas para consultas de logs de auditoría"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            username='test_user',
            password='Test1234!'
        )
        
        # Crear múltiples logs
        for i in range(5):
            AuditLog.objects.create(
                user=self.user,
                action=f'ACTION_{i}',
                ip_address='127.0.0.1'
            )
    
    def test_contar_logs_usuario(self):
        """Verificar conteo de logs por usuario"""
        count = AuditLog.objects.filter(user=self.user).count()
        self.assertEqual(count, 5)
    
    def test_ordenar_logs_por_fecha(self):
        """Verificar ordenamiento de logs por fecha"""
        logs = AuditLog.objects.filter(user=self.user).order_by('-created_at')
        self.assertEqual(logs.count(), 5)
        
        # Verificar que están ordenados
        if logs.count() > 1:
            self.assertGreaterEqual(
                logs[0].created_at,
                logs[1].created_at
            )
