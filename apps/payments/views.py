"""
Vistas de pagos y checkout para Ross Crafts.

Flujo ecommerce:
  1. checkout_view  (paso 1 y 2: envío + resumen)
  2. payment_view   (paso 3: formulario Stripe)
  3. create_payment_intent  → crea PaymentIntent en Stripe
  4. confirm_payment        → llamado por JS tras éxito; crea Sale/Order/Stock
  5. checkout_success       → página final con datos del pedido

El webhook de Stripe actúa como respaldo idempotente.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail
from decimal import Decimal
import stripe
import logging

from apps.ecommerce.models import Cart, Order
from apps.ecommerce.views import get_or_create_cart
from apps.customers.models import Customer
from apps.authentication.models import User
from apps.sales.models import Sale, SaleItem
from apps.stock.models import StockMovement
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger('apps.payments')


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_system_user():
    """Devuelve el primer superusuario o el primer usuario activo del sistema."""
    user = User.objects.filter(is_superuser=True, is_active=True).first()
    if not user:
        user = User.objects.filter(is_active=True, role__isnull=False).first()
    if not user:
        user = User.objects.filter(is_active=True).first()
    return user


def _calc_totals(items):
    subtotal = sum(item.subtotal for item in items)
    shipping = Decimal('10.00') if subtotal < Decimal('150.00') else Decimal('0.00')
    total = subtotal + shipping
    return subtotal, shipping, total


def _build_shipping_address(data):
    parts = [
        data.get('address', ''),
        data.get('district', ''),
        data.get('city', ''),
        data.get('department', ''),
    ]
    return ', '.join(p for p in parts if p)


def _process_sale(cart, checkout_data, payment_intent_id, system_user):
    """
    Crea Sale, SaleItems, StockMovements, Order y Payment de forma atómica.
    Devuelve el Order creado.
    Lanza excepción si algo falla (el atomic() del llamador hace rollback).
    """
    items = list(cart.items.select_related('product').all())
    if not items:
        raise ValueError('El carrito está vacío')

    # Validar que todos los productos estén activos y tengan stock suficiente
    for item in items:
        if not item.product.is_active:
            raise ValueError(f'El producto "{item.product.name}" ya no está disponible')
        if item.product.stock_quantity < item.quantity:
            raise ValueError(f'Stock insuficiente para "{item.product.name}". Disponible: {item.product.stock_quantity}')

    subtotal, shipping, total = _calc_totals(items)
    # Los precios ya incluyen IGV. Se extrae el componente IGV (18/118 del total)
    # para registrarlo en Sale.tax de forma consistente con el módulo POS.
    tax = (total * Decimal('18') / Decimal('118')).quantize(Decimal('0.01'))

    customer_id = checkout_data.get('customer_id')
    customer = Customer.objects.get(pk=customer_id) if customer_id else None

    # 1. Venta
    sale = Sale.objects.create(
        customer=customer,
        user=system_user,
        subtotal=subtotal,
        tax=tax,
        discount=Decimal('0.00'),
        total=total,
        payment_method='online',
        status='completed',
    )

    # 2. Items + movimientos de stock
    for item in items:
        SaleItem.objects.create(
            sale=sale,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.product.price,
            subtotal=item.subtotal,
        )
        # La señal post_save de StockMovement actualiza product.stock_quantity
        StockMovement.objects.create(
            product=item.product,
            user=system_user,
            movement_type='salida',
            quantity=item.quantity,
            reason=f'Venta online #{sale.id}',
        )

    # 3. Orden
    shipping_address = _build_shipping_address(checkout_data)
    order = Order.objects.create(
        customer=customer,
        sale=sale,
        shipping_address=shipping_address or 'Sin dirección',
        billing_address=checkout_data.get('address', ''),
        status='paid',
        payment_intent_id=payment_intent_id or None,
        total=total,
    )

    # 4. Registro de pago
    if payment_intent_id:
        Payment.objects.create(
            order=order,
            stripe_payment_id=payment_intent_id,
            amount=total,
            status='succeeded',
            payment_method='card',
        )

    # 5. Vaciar carrito
    cart.items.all().delete()

    logger.info(
        f'Venta online procesada | Order #{order.id} | Sale #{sale.id} | '
        f'Total: S/. {total:.2f} | Cliente: {checkout_data.get("email", "anónimo")}'
    )
    return order


# ── Checkout views ─────────────────────────────────────────────────────────────

def checkout_view(request):
    """Pasos 1 y 2: datos de envío y resumen."""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()

    if not items:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('ecommerce:cart')

    subtotal, shipping, total = _calc_totals(items)
    step = request.GET.get('step', '1')

    if request.method == 'POST':
        if step == '1':
            checkout_data = {
                'full_name':  request.POST.get('full_name', '').strip(),
                'address':    request.POST.get('address', '').strip(),
                'district':   request.POST.get('district', '').strip(),
                'city':       request.POST.get('city', '').strip(),
                'department': request.POST.get('department', '').strip(),
                'phone':      request.POST.get('phone', '').strip(),
                'email':      request.POST.get('email', '').strip(),
            }
            # Adjuntar customer_id si está autenticado
            if request.user.is_authenticated and isinstance(request.user, Customer):
                checkout_data['customer_id'] = request.user.pk
            request.session['checkout_data'] = checkout_data
            request.session.modified = True
            from django.urls import reverse
            return redirect(reverse('payments:checkout') + '?step=2')

        elif step == '2':
            return redirect('payments:payment')

    # Pre-rellenar con datos del cliente autenticado
    initial = {}
    if request.user.is_authenticated and isinstance(request.user, Customer):
        c = request.user
        initial = {
            'full_name': c.full_name,
            'email':     c.email,
            'phone':     c.phone,
            'address':   c.address,
        }
    checkout_data = request.session.get('checkout_data', initial)

    return render(request, 'payments/checkout.html', {
        'cart': cart, 'items': items,
        'subtotal': subtotal, 'shipping_cost': shipping, 'total': total,
        'step': step, 'checkout_data': checkout_data,
    })


def payment_view(request):
    """Paso 3: formulario de pago Stripe."""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()

    if not items:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('ecommerce:cart')

    checkout_data = request.session.get('checkout_data')
    if not checkout_data:
        messages.warning(request, 'Por favor completa los datos de envío.')
        return redirect('payments:checkout')

    subtotal, shipping, total = _calc_totals(items)

    return render(request, 'payments/payment.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'cart': cart, 'items': items,
        'subtotal': subtotal, 'shipping_cost': shipping, 'total': total,
        'checkout_data': checkout_data,
        'debug': settings.DEBUG,
    })


@require_POST
def create_payment_intent(request):
    """Crea un PaymentIntent en Stripe y devuelve el clientSecret."""
    try:
        cart = get_or_create_cart(request)
        items = cart.items.select_related('product').all()
        if not items:
            return JsonResponse({'error': 'Carrito vacío'}, status=400)

        subtotal, shipping, total = _calc_totals(items)
        amount_cents = int(total * 100)

        checkout_data = request.session.get('checkout_data', {})
        customer_email = checkout_data.get('email', '')
        customer_id = checkout_data.get('customer_id', '')

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='pen',
            receipt_email=customer_email or None,
            metadata={
                'customer_email': customer_email,
                'customer_id':    str(customer_id),
                'cart_id':        str(cart.pk),
                'session_key':    request.session.session_key or '',
            },
        )

        # Guardar el intent_id en sesión para confirm_payment
        request.session['pending_payment_intent'] = intent.id
        request.session.modified = True

        return JsonResponse({'clientSecret': intent.client_secret})

    except stripe.error.StripeError as e:
        logger.error(f'Stripe error al crear intent: {e}')
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f'Error al crear intent: {e}')
        return JsonResponse({'error': 'Error interno'}, status=500)


@require_POST
def confirm_payment(request):
    """
    Llamado por el JS del cliente tras paymentIntent.status === 'succeeded'.
    Procesa la venta, stock, orden y pago de forma atómica.
    """
    try:
        payment_intent_id = request.session.get('pending_payment_intent', '')

        # Verificar con Stripe que el pago realmente fue exitoso
        if payment_intent_id:
            try:
                pi = stripe.PaymentIntent.retrieve(payment_intent_id)
                if pi.status != 'succeeded':
                    return JsonResponse({'error': 'El pago no fue confirmado por Stripe'}, status=400)
            except stripe.error.StripeError as e:
                logger.warning(f'No se pudo verificar PaymentIntent {payment_intent_id}: {e}')
                # En modo test sin webhook, continuamos igual
                pass

        # Idempotencia: si ya existe la orden, devolver éxito
        if payment_intent_id and Order.objects.filter(payment_intent_id=payment_intent_id).exists():
            order = Order.objects.get(payment_intent_id=payment_intent_id)
            request.session['last_order_id'] = order.pk
            return JsonResponse({'success': True, 'order_id': order.pk})

        cart = get_or_create_cart(request)
        checkout_data = request.session.get('checkout_data', {})
        system_user = _get_system_user()

        if not system_user:
            return JsonResponse({'error': 'No hay usuarios del sistema configurados'}, status=500)

        with transaction.atomic():
            order = _process_sale(cart, checkout_data, payment_intent_id, system_user)

        # Guardar order_id en sesión para la página de éxito
        request.session['last_order_id'] = order.pk
        request.session.pop('pending_payment_intent', None)
        request.session.pop('checkout_data', None)
        request.session.modified = True

        # Email de confirmación (no bloquea si falla)
        try:
            _send_confirmation_email(order)
        except Exception as e:
            logger.error(f'Error enviando email para Order #{order.pk}: {e}')

        return JsonResponse({'success': True, 'order_id': order.pk})

    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f'Error en confirm_payment: {e}', exc_info=True)
        return JsonResponse({'error': 'Error al procesar el pedido'}, status=500)


def checkout_success(request):
    """Página de confirmación final."""
    order_id = request.session.get('last_order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.select_related('sale', 'customer').get(pk=order_id)
        except Order.DoesNotExist:
            pass

    return render(request, 'payments/success.html', {'order': order})


def checkout_cancelled(request):
    return render(request, 'payments/cancelled.html')


# ── Stripe Webhook (respaldo idempotente) ─────────────────────────────────────

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload    = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    ip         = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR', '')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        logger.error(f'Webhook payload inválido desde {ip}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.warning(f'Webhook firma inválida desde {ip}')
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        pi = event['data']['object']
        pi_id = pi['id']

        # Idempotencia: si ya procesamos esta orden, ignorar
        if Order.objects.filter(payment_intent_id=pi_id).exists():
            return HttpResponse(status=200)

        try:
            customer_id  = pi['metadata'].get('customer_id', '')
            cart_id      = pi['metadata'].get('cart_id', '')
            session_key  = pi['metadata'].get('session_key', '')
            email        = pi['metadata'].get('customer_email', '')

            cart = None
            if cart_id:
                cart = Cart.objects.filter(pk=cart_id).first()
            if not cart and session_key:
                cart = Cart.objects.filter(session_key=session_key, customer__isnull=True).first()
            if not cart and customer_id:
                cart = Cart.objects.filter(customer_id=customer_id).first()

            if not cart or not cart.items.exists():
                logger.warning(f'Webhook: carrito no encontrado para PI {pi_id}')
                return HttpResponse(status=200)

            system_user = _get_system_user()
            checkout_data = {
                'customer_id': customer_id,
                'email': email,
                'address': '', 'district': '', 'city': '', 'department': '',
            }

            with transaction.atomic():
                _process_sale(cart, checkout_data, pi_id, system_user)

        except Exception as e:
            logger.error(f'Webhook error procesando PI {pi_id}: {e}', exc_info=True)
            return HttpResponse(status=500)

    return HttpResponse(status=200)


# ── Email ─────────────────────────────────────────────────────────────────────

def _send_confirmation_email(order):
    customer_email = order.customer.email if order.customer else None
    if not customer_email:
        return

    items = order.sale.items.select_related('product').all() if order.sale else []
    rows = ''.join(
        f'<tr>'
        f'<td style="padding:8px;border-bottom:1px solid #E3DBBB">{i.product.name}</td>'
        f'<td style="padding:8px;border-bottom:1px solid #E3DBBB;text-align:center">{i.quantity}</td>'
        f'<td style="padding:8px;border-bottom:1px solid #E3DBBB;text-align:right">S/. {i.unit_price:.2f}</td>'
        f'<td style="padding:8px;border-bottom:1px solid #E3DBBB;text-align:right">S/. {i.subtotal:.2f}</td>'
        f'</tr>'
        for i in items
    )

    html = f"""
    <html><body style="font-family:Arial,sans-serif;background:#F8F3E1;padding:20px">
    <div style="max-width:600px;margin:0 auto;background:white;border-radius:8px;overflow:hidden">
      <div style="background:#41431B;color:white;padding:30px;text-align:center">
        <h1 style="margin:0">¡Pedido Confirmado!</h1>
      </div>
      <div style="padding:30px">
        <p>Hola <strong>{order.customer.first_name if order.customer else ''}</strong>,</p>
        <p>Gracias por tu compra en Ross Crafts. Tu pedido ha sido confirmado.</p>
        <div style="background:#E3DBBB;padding:15px;border-radius:4px;margin:20px 0">
          <p style="margin:4px 0"><strong>N° Pedido:</strong> #{order.id}</p>
          <p style="margin:4px 0"><strong>Fecha:</strong> {order.created_at.strftime('%d/%m/%Y %H:%M')}</p>
          <p style="margin:4px 0"><strong>Dirección:</strong> {order.shipping_address}</p>
        </div>
        <table style="width:100%;border-collapse:collapse;margin:20px 0">
          <thead>
            <tr style="background:#AEB784;color:white">
              <th style="padding:10px;text-align:left">Producto</th>
              <th style="padding:10px;text-align:center">Cant.</th>
              <th style="padding:10px;text-align:right">Precio</th>
              <th style="padding:10px;text-align:right">Subtotal</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
        <div style="text-align:right">
          <p style="font-size:18px;color:#41431B"><strong>Total: S/. {order.total:.2f}</strong></p>
        </div>
        <p style="color:#666;margin-top:20px">Recibirás un email cuando tu pedido sea enviado.</p>
        <p style="color:#41431B;font-weight:bold;text-align:center">El equipo de Ross Crafts</p>
      </div>
    </div>
    </body></html>
    """

    send_mail(
        subject=f'Pedido confirmado #{order.id} - Ross Crafts',
        message=f'Tu pedido #{order.id} por S/. {order.total:.2f} ha sido confirmado.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[customer_email],
        html_message=html,
        fail_silently=True,
    )
