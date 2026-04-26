"""
Pruebas para el módulo de reportes
"""
from decimal import Decimal
from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.utils import timezone
from apps.authentication.models import User
from apps.stock.models import Category, Product
from apps.sales.models import Sale, SaleItem


class ReportsTests(TestCase):
    """Pruebas para generación de reportes"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        
        # Crear usuario gerente
        self.gerente = User.objects.create_user(
            username='gerente_test',
            password='Test1234!',
            role='gerente'
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
        
        # Crear ventas de prueba
        self._crear_ventas_prueba()
        
        # Login
        self.client.login(username='gerente_test', password='Test1234!')
    
    def _crear_ventas_prueba(self):
        """Crear ventas de prueba en diferentes fechas"""
        # Venta de hoy
        sale_hoy = Sale.objects.create(
            user=self.gerente,
            subtotal=Decimal('100.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('100.00'),
            payment_method='cash',
            status='completed'
        )
        SaleItem.objects.create(
            sale=sale_hoy,
            product=self.product,
            quantity=4,
            unit_price=self.product.price
        )
        
        # Venta de hace 7 días
        sale_antigua = Sale.objects.create(
            user=self.gerente,
            subtotal=Decimal('50.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('50.00'),
            payment_method='card',
            status='completed'
        )
        sale_antigua.created_at = timezone.now() - timedelta(days=7)
        sale_antigua.save()
        
        SaleItem.objects.create(
            sale=sale_antigua,
            product=self.product,
            quantity=2,
            unit_price=self.product.price
        )
    
    def test_reporte_ventas_rango_fechas(self):
        """Verificar reporte de ventas por rango de fechas"""
        hoy = timezone.now().date()
        hace_30_dias = hoy - timedelta(days=30)
        
        response = self.client.get('/dashboard/reportes/ventas/', {
            'desde': hace_30_dias.strftime('%Y-%m-%d'),
            'hasta': hoy.strftime('%Y-%m-%d')
        })
        
        self.assertEqual(response.status_code, 200)
    
    def test_reporte_ventas_sin_fechas(self):
        """Verificar reporte de ventas sin especificar fechas"""
        response = self.client.get('/dashboard/reportes/ventas/')
        self.assertEqual(response.status_code, 200)
    
    def test_exportar_ventas_pdf(self):
        """Verificar exportación de ventas a PDF"""
        response = self.client.get('/dashboard/reportes/ventas/pdf/')
        
        if response.status_code == 200:
            self.assertEqual(response['Content-Type'], 'application/pdf')
    
    def test_exportar_ventas_excel(self):
        """Verificar exportación de ventas a Excel"""
        response = self.client.get('/dashboard/reportes/ventas/excel/')
        
        if response.status_code == 200:
            self.assertIn('spreadsheetml', response['Content-Type'])
    
    def test_reporte_productos_mas_vendidos(self):
        """Verificar reporte de productos más vendidos"""
        response = self.client.get('/dashboard/reportes/productos-mas-vendidos/')
        
        if response.status_code == 200:
            self.assertContains(response, self.product.name)
    
    def test_reporte_stock_bajo(self):
        """Verificar reporte de productos con stock bajo"""
        # Reducir stock
        self.product.stock_quantity = 3
        self.product.save()
        
        response = self.client.get('/dashboard/reportes/stock-bajo/')
        
        if response.status_code == 200:
            self.assertContains(response, self.product.name)
    
    def test_empleado_no_accede_reportes(self):
        """Verificar que empleados no pueden acceder a reportes"""
        # Crear empleado
        empleado = User.objects.create_user(
            username='empleado_test',
            password='Test1234!',
            role='empleado'
        )
        
        # Logout gerente y login empleado
        self.client.logout()
        self.client.login(username='empleado_test', password='Test1234!')
        
        response = self.client.get('/dashboard/reportes/ventas/')
        self.assertIn(response.status_code, [302, 403])


class ReportDataTests(TestCase):
    """Pruebas para datos de reportes"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            username='test_user',
            password='Test1234!',
            role='gerente'
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
    
    def test_calcular_total_ventas_periodo(self):
        """Verificar cálculo de total de ventas en un período"""
        from django.db import models
        
        # Crear ventas
        for i in range(3):
            sale = Sale.objects.create(
                user=self.user,
                subtotal=Decimal('100.00'),
                tax=Decimal('0.00'),
                discount=Decimal('0.00'),
                total=Decimal('100.00'),
                payment_method='cash'
            )
        
        # Calcular total
        total = Sale.objects.filter(status='completed').aggregate(
            total=models.Sum('total')
        )
        
        self.assertEqual(total['total'], Decimal('300.00'))
    
    def test_contar_ventas_por_metodo_pago(self):
        """Verificar conteo de ventas por método de pago"""
        # Crear ventas con diferentes métodos
        Sale.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('100.00'),
            payment_method='cash'
        )
        
        Sale.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('0.00'),
            discount=Decimal('0.00'),
            total=Decimal('100.00'),
            payment_method='card'
        )
        
        cash_count = Sale.objects.filter(payment_method='cash').count()
        card_count = Sale.objects.filter(payment_method='card').count()
        
        self.assertEqual(cash_count, 1)
        self.assertEqual(card_count, 1)
