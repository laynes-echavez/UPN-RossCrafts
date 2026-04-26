"""
Script para verificar que los templates se renderizan correctamente
"""
from django.template import Template, Context
from django.template.loader import get_template
from django.conf import settings
import os
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
import django
django.setup()

def test_template(template_name):
    """Probar que un template se puede cargar sin errores"""
    try:
        template = get_template(template_name)
        print(f"✅ {template_name} - OK")
        return True
    except Exception as e:
        print(f"❌ {template_name} - ERROR: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("VERIFICACIÓN DE TEMPLATES")
    print("=" * 60)
    
    templates_to_test = [
        'store/base_store.html',
        'store/home.html',
        'store/catalog.html',
        'store/product_detail.html',
        'store/cart.html',
        'base.html',
        'authentication/login.html',
    ]
    
    results = []
    for template_name in templates_to_test:
        result = test_template(template_name)
        results.append(result)
    
    print("=" * 60)
    print(f"RESULTADO: {sum(results)}/{len(results)} templates OK")
    print("=" * 60)
    
    if all(results):
        print("✅ Todos los templates se cargan correctamente")
        sys.exit(0)
    else:
        print("❌ Algunos templates tienen errores")
        sys.exit(1)
