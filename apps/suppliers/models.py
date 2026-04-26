from django.db import models


class Supplier(models.Model):
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=500, blank=True)
    ruc = models.CharField(max_length=11, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rc_suppliers'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['company_name']
    
    def __str__(self):
        return self.company_name


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('received', 'Recibida'),
        ('cancelled', 'Cancelada'),
    ]
    
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    notes = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rc_purchase_orders'
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OC-{self.id} - {self.supplier.company_name}"


class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('stock.Product', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        db_table = 'rc_purchase_order_items'
        verbose_name = 'Item de Orden de Compra'
        verbose_name_plural = 'Items de Órdenes de Compra'
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_cost
        super().save(*args, **kwargs)
