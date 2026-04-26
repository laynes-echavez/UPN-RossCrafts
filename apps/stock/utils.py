"""
Utilidades para la gestión de stock
"""
import openpyxl
from .models import Product, Category, StockMovement
from django.db import transaction


def import_products_from_excel(file, user):
    """
    Importa productos desde un archivo Excel
    
    Columnas esperadas:
    - Nombre
    - SKU
    - Categoría
    - Precio
    - Costo
    - Stock Actual
    - Stock Mínimo
    
    Returns:
        dict: {
            'created': int,
            'updated': int,
            'errors': list
        }
    """
    result = {
        'created': 0,
        'updated': 0,
        'errors': []
    }
    
    try:
        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        
        # Verificar encabezados
        headers = [cell.value for cell in sheet[1]]
        expected_headers = ['Nombre', 'SKU', 'Categoría', 'Precio', 'Costo', 'Stock Actual', 'Stock Mínimo']
        
        if headers[:7] != expected_headers:
            result['errors'].append(
                f'Encabezados incorrectos. Se esperan: {", ".join(expected_headers)}'
            )
            return result
        
        # Procesar filas
        for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):  # Saltar filas vacías
                continue
            
            try:
                with transaction.atomic():
                    nombre, sku, categoria_nombre, precio, costo, stock_actual, stock_minimo = row[:7]
                    
                    # Validar datos requeridos
                    if not nombre or not sku:
                        result['errors'].append(f'Fila {row_num}: Nombre y SKU son requeridos')
                        continue
                    
                    # Obtener o crear categoría
                    if categoria_nombre:
                        category, _ = Category.objects.get_or_create(
                            name=categoria_nombre,
                            defaults={'description': f'Categoría {categoria_nombre}'}
                        )
                    else:
                        category = Category.objects.first()
                        if not category:
                            category = Category.objects.create(
                                name='General',
                                description='Categoría general'
                            )
                    
                    # Crear o actualizar producto
                    product, created = Product.objects.get_or_create(
                        sku=sku,
                        defaults={
                            'name': nombre,
                            'category': category,
                            'price': precio or 0,
                            'cost_price': costo or 0,
                            'stock_quantity': stock_actual or 0,
                            'min_stock_quantity': stock_minimo or 5,
                        }
                    )
                    
                    if created:
                        result['created'] += 1
                        # Registrar movimiento inicial
                        if stock_actual and stock_actual > 0:
                            StockMovement.objects.create(
                                product=product,
                                user=user,
                                movement_type='ajuste',
                                quantity=stock_actual,
                                previous_quantity=0,
                                new_quantity=stock_actual,
                                reason='Importación inicial desde Excel'
                            )
                    else:
                        # Actualizar producto existente
                        updated = False
                        
                        if nombre and product.name != nombre:
                            product.name = nombre
                            updated = True
                        
                        if precio and product.price != precio:
                            product.price = precio
                            updated = True
                        
                        if costo and product.cost_price != costo:
                            product.cost_price = costo
                            updated = True
                        
                        if stock_minimo and product.min_stock_quantity != stock_minimo:
                            product.min_stock_quantity = stock_minimo
                            updated = True
                        
                        # Actualizar stock si cambió
                        if stock_actual is not None and product.stock_quantity != stock_actual:
                            old_stock = product.stock_quantity
                            product.stock_quantity = stock_actual
                            updated = True
                            
                            # Registrar movimiento de ajuste
                            StockMovement.objects.create(
                                product=product,
                                user=user,
                                movement_type='ajuste',
                                quantity=stock_actual,
                                previous_quantity=old_stock,
                                new_quantity=stock_actual,
                                reason='Actualización desde Excel'
                            )
                        
                        if updated:
                            product.save()
                            result['updated'] += 1
            
            except Exception as e:
                result['errors'].append(f'Fila {row_num}: {str(e)}')
    
    except Exception as e:
        result['errors'].append(f'Error al leer el archivo: {str(e)}')
    
    return result
