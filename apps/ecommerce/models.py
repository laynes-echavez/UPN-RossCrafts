from django.db import models


class Cart(models.Model):
    session_key = models.CharField(max_length=100, blank=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, 
                                 null=True, blank=True, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rc_carts'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.customer:
            return f"Carrito de {self.customer.full_name}"
        return f"Carrito #{self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('stock.Product', on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'rc_cart_items'
        verbose_name = 'Item de Carrito'
        verbose_name_plural = 'Items de Carrito'
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT,
                                 null=True, blank=True, related_name='orders')
    sale = models.OneToOneField('sales.Sale', on_delete=models.SET_NULL, 
                                null=True, blank=True, related_name='order')
    shipping_address = models.CharField(max_length=500)
    billing_address = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    payment_intent_id = models.CharField(max_length=200, blank=True, null=True, unique=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rc_orders'
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-created_at']
    
    def __str__(self):
        name = self.customer.full_name if self.customer else 'Anónimo'
        return f"Orden #{self.id} - {name}"
