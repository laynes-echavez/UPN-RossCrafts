"""
Señales para actualizar automáticamente el stock
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockMovement
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=StockMovement)
def update_product_stock(sender, instance, created, **kwargs):
    """
    Actualiza el stock del producto cuando se crea un movimiento
    """
    if created:
        product = instance.product
        
        # Guardar cantidad anterior
        previous_qty = product.stock_quantity
        
        # Calcular nueva cantidad según tipo de movimiento
        if instance.movement_type == 'entrada':
            new_qty = previous_qty + instance.quantity
        elif instance.movement_type == 'salida':
            new_qty = previous_qty - instance.quantity
        elif instance.movement_type == 'ajuste':
            new_qty = instance.quantity
        else:
            new_qty = previous_qty
        
        # Actualizar stock del producto
        product.stock_quantity = new_qty
        product.save(update_fields=['stock_quantity', 'updated_at'])
        
        # Actualizar campos del movimiento
        instance.previous_quantity = previous_qty
        instance.new_quantity = new_qty
        StockMovement.objects.filter(pk=instance.pk).update(
            previous_quantity=previous_qty,
            new_quantity=new_qty
        )
        
        # Log
        logger.info(
            f'Stock actualizado: {product.name} (SKU: {product.sku}) '
            f'- Anterior: {previous_qty}, Nuevo: {new_qty}, '
            f'Tipo: {instance.movement_type}, Usuario: {instance.user.username}'
        )
