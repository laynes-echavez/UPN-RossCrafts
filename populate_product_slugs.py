"""
Script para poblar los slugs de productos existentes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from apps.stock.models import Product
from django.utils.text import slugify


def populate_slugs():
    print("Poblando slugs de productos...")
    
    products = Product.objects.all()
    updated = 0
    
    for product in products:
        if not product.slug:
            base_slug = slugify(product.name)
            slug = base_slug
            counter = 1
            
            # Asegurar que el slug sea único
            while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            product.slug = slug
            product.save(update_fields=['slug'])
            updated += 1
            print(f"  ✓ {product.name} → {slug}")
    
    print(f"\n{updated} productos actualizados")


if __name__ == '__main__':
    populate_slugs()
