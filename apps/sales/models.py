from django.db import models
from django.utils import timezone


class Sale(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
        ('online', 'Pago Online'),
    ]
    
    STATUS_CHOICES = [
        ('completed', 'Completada'),
        ('pending', 'Pendiente'),
        ('cancelled', 'Cancelada'),
        ('refunded', 'Reembolsada'),
    ]
    
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, 
                                 null=True, blank=True, related_name='sales')
    user = models.ForeignKey('authentication.User', on_delete=models.PROTECT)
    receipt_number = models.CharField(max_length=50, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rc_sales'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Venta #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            # Generar número de comprobante: RC-YYYY-XXXXXX
            from django.db import transaction
            with transaction.atomic():
                year = timezone.now().year
                # Usar select_for_update para evitar race conditions
                last_sale = Sale.objects.filter(
                    receipt_number__startswith=f'RC-{year}-'
                ).select_for_update().order_by('-id').first()
                
                if last_sale and last_sale.receipt_number:
                    last_number = int(last_sale.receipt_number.split('-')[-1])
                    new_number = last_number + 1
                else:
                    new_number = 1
                
                self.receipt_number = f'RC-{year}-{new_number:06d}'
        
        super().save(*args, **kwargs)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('stock.Product', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        db_table = 'rc_sale_items'
        verbose_name = 'Item de Venta'
        verbose_name_plural = 'Items de Ventas'
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
