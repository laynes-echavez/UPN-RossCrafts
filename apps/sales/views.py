from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.db.models import F
from apps.authentication.decorators import role_required
from .models import Sale, SaleItem
from apps.stock.models import Product, StockMovement
from apps.customers.models import Customer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
from datetime import datetime
from decimal import Decimal
import logging

# Configurar logger para ventas
logger = logging.getLogger('apps.sales')


@login_required
@role_required(['gerente', 'administrador', 'empleado'])
def pos_view(request):
    """Vista principal del punto de venta"""
    return render(request, 'sales/pos.html')


@login_required
@require_POST
def register_sale(request):
    """Registrar una nueva venta"""
    try:
        import json
        data = json.loads(request.body)
        
        # Validar datos
        items = data.get('items', [])
        if not items:
            return JsonResponse({'success': False, 'error': 'El carrito está vacío'})
        
        customer_id = data.get('customer_id')
        payment_method = data.get('payment_method', 'cash')
        discount_amount = Decimal(str(data.get('discount', 0)))
        discount_type = data.get('discount_type', 'fixed')  # fixed o percentage
        
        with transaction.atomic():
            # Validar stock disponible
            for item in items:
                product = Product.objects.select_for_update().get(id=item['product_id'])
                if product.stock_quantity < item['quantity']:
                    return JsonResponse({
                        'success': False,
                        'error': f'Stock insuficiente para {product.name}. Disponible: {product.stock_quantity}'
                    })
            
            # Calcular totales
            subtotal = Decimal('0')
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                subtotal += product.price * item['quantity']
            
            # Calcular descuento
            if discount_type == 'percentage':
                discount = subtotal * (discount_amount / 100)
            else:
                discount = discount_amount
            
            # Calcular IGV (18%)
            subtotal_after_discount = subtotal - discount
            tax = subtotal_after_discount * Decimal('0.18')
            total = subtotal_after_discount + tax
            
            # Crear venta
            sale = Sale.objects.create(
                customer_id=customer_id if customer_id else None,
                user=request.user,
                subtotal=subtotal,
                tax=tax,
                discount=discount,
                total=total,
                payment_method=payment_method,
                status='completed'
            )
            
            # Crear items de venta y movimientos de stock
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']
                unit_price = product.price
                item_subtotal = unit_price * quantity
                
                # Crear item de venta
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=item_subtotal
                )
                
                # Crear movimiento de stock (la señal actualizará el stock)
                StockMovement.objects.create(
                    product=product,
                    user=request.user,
                    movement_type='salida',
                    quantity=quantity,
                    reason=f'Venta #{sale.id}'
                )
            
            # Generar número de comprobante
            year = datetime.now().year
            comprobante = f'RC-{year}-{sale.id:06d}'
            
            # Registrar en log de actividad
            logger.info(
                f"Venta #{sale.id} registrada por {request.user.username} | "
                f"Total: S/. {sale.total:.2f} | Cliente: {sale.customer.full_name if sale.customer else 'Sin cliente'}"
            )
            
            return JsonResponse({
                'success': True,
                'sale_id': sale.id,
                'comprobante': comprobante,
                'total': str(total)
            })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def sale_receipt_pdf(request, sale_id):
    """Generar comprobante de venta en PDF"""
    sale = get_object_or_404(Sale, id=sale_id)
    
    # Crear buffer
    buffer = BytesIO()
    
    # Crear PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#41431B'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    # Título
    elements.append(Paragraph('COMPROBANTE DE VENTA', title_style))
    elements.append(Paragraph('Ross Crafts', styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Número de comprobante
    year = sale.created_at.year
    comprobante = f'RC-{year}-{sale.id:06d}'
    elements.append(Paragraph(f'<b>Comprobante:</b> {comprobante}', styles['Normal']))
    elements.append(Paragraph(f'<b>Fecha:</b> {sale.created_at.strftime("%d/%m/%Y %H:%M")}', styles['Normal']))
    elements.append(Paragraph(f'<b>Atendido por:</b> {sale.user.get_full_name() or sale.user.username}', styles['Normal']))
    
    # Datos del cliente
    if sale.customer:
        elements.append(Paragraph(f'<b>Cliente:</b> {sale.customer.full_name}', styles['Normal']))
        if sale.customer.dni:
            elements.append(Paragraph(f'<b>DNI:</b> {sale.customer.dni}', styles['Normal']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de productos
    data = [['Descripción', 'Cant.', 'P.Unit', 'Subtotal']]
    
    for item in sale.items.all():
        data.append([
            item.product.name,
            str(item.quantity),
            f'S/. {item.unit_price:.2f}',
            f'S/. {item.subtotal:.2f}'
        ])
    
    table = Table(data, colWidths=[3.5*inch, 0.8*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#41431B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Totales
    totals_style = ParagraphStyle('Totals', parent=styles['Normal'], alignment=TA_RIGHT)
    elements.append(Paragraph(f'<b>Subtotal:</b> S/. {sale.subtotal:.2f}', totals_style))
    if sale.discount > 0:
        elements.append(Paragraph(f'<b>Descuento:</b> - S/. {sale.discount:.2f}', totals_style))
    elements.append(Paragraph(f'<b>IGV (18%):</b> S/. {sale.tax:.2f}', totals_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(f'<b><font size=14>TOTAL: S/. {sale.total:.2f}</font></b>', totals_style))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f'<b>Método de pago:</b> {sale.get_payment_method_display()}', styles['Normal']))
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)
    elements.append(Paragraph('Gracias por su compra - Ross Crafts', footer_style))
    
    # Construir PDF
    doc.build(elements)
    
    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="comprobante_{comprobante}.pdf"'
    
    return response


@login_required
@require_POST
def quick_customer_register(request):
    """Registro rápido de cliente desde POS"""
    try:
        import json
        data = json.loads(request.body)
        
        customer = Customer.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            dni=data.get('dni', '')
        )
        
        return JsonResponse({
            'success': True,
            'customer': {
                'id': customer.id,
                'full_name': customer.full_name,
                'email': customer.email,
                'dni': customer.dni,
                'phone': customer.phone
            }
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
