#!/usr/bin/env python
"""
Script de validación de flujos del sistema Ross Crafts.
Ejecuta verificaciones automáticas para detectar problemas en los flujos críticos.

Uso:
    python validate_system_flows.py
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')
django.setup()

from django.db import transaction
from django.contrib.auth import get_user_model
from apps.stock.models import Product, Category, StockMovement
from apps.customers.models import Customer
from apps.sales.models import Sale, SaleItem
from apps.ecommerce.models import Cart, CartItem, Order
from apps.payments.models import Payment
from apps.suppliers.models import Supplier, PurchaseOrder
from apps.audit.models import AuditLog

User = get_user_model()

class SystemValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []
    
    def log_error(self, test_name, message):
        self.errors.append(f"❌ {test_name}: {message}")
    
    def log_warning(self, test_name, message):
        self.warnings.append(f"⚠️  {test_name}: {message}")
    
    def log_pass(self, test_name, message="OK"):
        self.passed.append(f"✅ {test_name}: {message}")
    
    def validate_user_system(self):
        """Validar que existe al menos un usuario del sistema"""
        try:
            system_users = User.objects.filter(is_active=True, is_superuser=True)
            if not system_users.exists():
                active_users = User.objects.filter(is_active=True)
                if not active_users.exists():
                    self.log_error("Sistema de Usuarios", "No hay usuarios activos en el sistema")
                else:
                    self.log_warning("Sistema de Usuarios", "No hay superusuarios, solo usuarios normales")
            else:
                self.log_pass("Sistema de Usuarios", f"{system_users.count()} superusuarios activos")
        except Exception as e:
            self.log_error("Sistema de Usuarios", f"Error al validar: {e}")
    
    def validate_stock_signals(self):
        """Validar que las señales de stock funcionan correctamente"""
        try:
            # Buscar un producto existente o crear uno de prueba
            product = Product.objects.filter(is_active=True).first()
            if not product:
                self.log_warning("Señales de Stock", "No hay productos para probar")
                return
            
            initial_stock = product.stock_quantity
            test_quantity = 5
            
            # Crear usuario de prueba si no existe
            user = User.objects.filter(is_active=True).first()
            if not user:
                self.log_error("Señales de Stock", "No hay usuarios para crear movimiento")
                return
            
            # Crear movimiento de entrada
            with transaction.atomic():
                movement = StockMovement.objects.create(
                    product=product,
                    user=user,
                    movement_type='entrada',
                    quantity=test_quantity,
                    reason='Validación automática del sistema'
                )
                
                # Refrescar producto desde BD
                product.refresh_from_db()
                expected_stock = initial_stock + test_quantity
                
                if product.stock_quantity == expected_stock:
                    self.log_pass("Señales de Stock", "Actualización automática funciona correctamente")
                else:
                    self.log_error("Señales de Stock", 
                                 f"Stock no actualizado. Esperado: {expected_stock}, Actual: {product.stock_quantity}")
                
                # Revertir cambios
                movement.delete()
                product.stock_quantity = initial_stock
                product.save()
                
        except Exception as e:
            self.log_error("Señales de Stock", f"Error al validar: {e}")
    
    def validate_cart_system(self):
        """Validar que el sistema de carrito funciona"""
        try:
            # Verificar que hay productos disponibles
            products = Product.objects.filter(is_active=True, stock_quantity__gt=0)
            if not products.exists():
                self.log_warning("Sistema de Carrito", "No hay productos con stock para probar")
                return
            
            product = products.first()
            
            # Crear carrito de prueba
            cart = Cart.objects.create(session_key='test_validation_session')
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1
            )
            
            # Validar cálculo de subtotal
            expected_subtotal = product.price * 1
            if cart_item.subtotal == expected_subtotal:
                self.log_pass("Sistema de Carrito", "Cálculo de subtotales correcto")
            else:
                self.log_error("Sistema de Carrito", 
                             f"Subtotal incorrecto. Esperado: {expected_subtotal}, Actual: {cart_item.subtotal}")
            
            # Limpiar
            cart.delete()
            
        except Exception as e:
            self.log_error("Sistema de Carrito", f"Error al validar: {e}")
    
    def validate_receipt_numbering(self):
        """Validar que la numeración de comprobantes es única"""
        try:
            # Verificar que no hay duplicados en receipt_number
            from django.db.models import Count
            duplicates = Sale.objects.values('receipt_number').annotate(
                count=Count('receipt_number')
            ).filter(count__gt=1, receipt_number__isnull=False)
            
            if duplicates.exists():
                self.log_error("Numeración de Comprobantes", 
                             f"Encontrados {duplicates.count()} números duplicados")
            else:
                self.log_pass("Numeración de Comprobantes", "No hay duplicados")
                
        except Exception as e:
            self.log_error("Numeración de Comprobantes", f"Error al validar: {e}")
    
    def validate_foreign_keys(self):
        """Validar integridad de claves foráneas críticas"""
        try:
            # Verificar órdenes huérfanas
            orphaned_orders = Order.objects.filter(sale__isnull=True).count()
            if orphaned_orders > 0:
                self.log_warning("Integridad FK", f"{orphaned_orders} órdenes sin venta asociada")
            else:
                self.log_pass("Integridad FK", "Todas las órdenes tienen venta asociada")
            
            # Verificar pagos huérfanos
            orphaned_payments = Payment.objects.filter(order__isnull=True).count()
            if orphaned_payments > 0:
                self.log_error("Integridad FK", f"{orphaned_payments} pagos sin orden asociada")
            else:
                self.log_pass("Integridad FK", "Todos los pagos tienen orden asociada")
                
        except Exception as e:
            self.log_error("Integridad FK", f"Error al validar: {e}")
    
    def validate_audit_system(self):
        """Validar que el sistema de auditoría funciona"""
        try:
            # Verificar que hay logs recientes
            from django.utils import timezone
            from datetime import timedelta
            
            recent_logs = AuditLog.objects.filter(
                timestamp__gte=timezone.now() - timedelta(days=7)
            ).count()
            
            if recent_logs > 0:
                self.log_pass("Sistema de Auditoría", f"{recent_logs} logs en los últimos 7 días")
            else:
                self.log_warning("Sistema de Auditoría", "No hay logs recientes")
                
        except Exception as e:
            self.log_error("Sistema de Auditoría", f"Error al validar: {e}")
    
    def validate_stock_consistency(self):
        """Validar consistencia entre movimientos y stock actual"""
        try:
            inconsistent_products = []
            
            for product in Product.objects.filter(is_active=True)[:10]:  # Muestra de 10 productos
                # Calcular stock basado en movimientos
                movements = StockMovement.objects.filter(product=product).order_by('created_at')
                calculated_stock = 0
                
                for movement in movements:
                    if movement.movement_type == 'entrada':
                        calculated_stock += movement.quantity
                    elif movement.movement_type == 'salida':
                        calculated_stock -= movement.quantity
                    elif movement.movement_type == 'ajuste':
                        calculated_stock = movement.quantity
                
                if calculated_stock != product.stock_quantity:
                    inconsistent_products.append(
                        f"{product.name}: DB={product.stock_quantity}, Calculado={calculated_stock}"
                    )
            
            if inconsistent_products:
                self.log_error("Consistencia de Stock", 
                             f"{len(inconsistent_products)} productos inconsistentes")
                for prod in inconsistent_products[:3]:  # Mostrar solo los primeros 3
                    print(f"    {prod}")
            else:
                self.log_pass("Consistencia de Stock", "Stock consistente con movimientos")
                
        except Exception as e:
            self.log_error("Consistencia de Stock", f"Error al validar: {e}")
    
    def run_all_validations(self):
        """Ejecutar todas las validaciones"""
        print("🔍 Iniciando validación de flujos del sistema Ross Crafts...\n")
        
        self.validate_user_system()
        self.validate_stock_signals()
        self.validate_cart_system()
        self.validate_receipt_numbering()
        self.validate_foreign_keys()
        self.validate_audit_system()
        self.validate_stock_consistency()
        
        # Mostrar resultados
        print("\n" + "="*60)
        print("📊 RESULTADOS DE LA VALIDACIÓN")
        print("="*60)
        
        if self.passed:
            print(f"\n✅ PRUEBAS EXITOSAS ({len(self.passed)}):")
            for test in self.passed:
                print(f"  {test}")
        
        if self.warnings:
            print(f"\n⚠️  ADVERTENCIAS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.errors:
            print(f"\n❌ ERRORES CRÍTICOS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
        
        print(f"\n📈 RESUMEN:")
        print(f"  • Pruebas exitosas: {len(self.passed)}")
        print(f"  • Advertencias: {len(self.warnings)}")
        print(f"  • Errores críticos: {len(self.errors)}")
        
        if self.errors:
            print(f"\n🚨 ACCIÓN REQUERIDA: Se encontraron {len(self.errors)} errores críticos que requieren atención inmediata.")
            return False
        elif self.warnings:
            print(f"\n⚠️  REVISIÓN RECOMENDADA: Se encontraron {len(self.warnings)} advertencias que deberían revisarse.")
            return True
        else:
            print(f"\n🎉 SISTEMA SALUDABLE: Todos los flujos críticos funcionan correctamente.")
            return True

if __name__ == "__main__":
    validator = SystemValidator()
    success = validator.run_all_validations()
    sys.exit(0 if success else 1)