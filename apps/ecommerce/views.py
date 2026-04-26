from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q, Sum
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from apps.stock.models import Product, Category
from apps.customers.models import Customer
from apps.sales.models import Sale
from .models import Cart, CartItem, Order
from .forms import (
    CustomerRegisterForm, CustomerLoginForm, CustomerProfileForm,
    CustomerChangePasswordForm, CustomerPasswordResetForm
)
from .decorators import customer_login_required
from decimal import Decimal


def get_or_create_cart(request):
    """Obtener o crear carrito para el usuario/sesión"""
    from apps.customers.models import Customer as CustomerModel
    if request.user.is_authenticated and isinstance(request.user, CustomerModel):
        # Cliente autenticado
        cart, _ = Cart.objects.get_or_create(customer=request.user, session_key='')
        return cart

    # Usuario anónimo o staff — usar sesión
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Tomar el más reciente si hay duplicados, o crear uno nuevo
    cart = Cart.objects.filter(session_key=session_key, customer__isnull=True).order_by('-created_at').first()
    if not cart:
        cart = Cart.objects.create(session_key=session_key)
    return cart


@ensure_csrf_cookie
def store_home(request):
    """Página de inicio de la tienda"""
    # Categorías activas
    categories = Category.objects.filter(is_active=True).order_by('name')[:6]
    
    # Productos destacados (más recientes con stock)
    featured_products = Product.objects.filter(
        is_active=True,
        stock_quantity__gt=0
    ).order_by('-created_at')[:4]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    
    return render(request, 'store/home.html', context)


def store_catalog(request):
    """Catálogo de productos con filtros"""
    # Asegurar que la sesión existe para el carrito anónimo
    if not request.session.session_key:
        request.session.create()
    products = Product.objects.filter(is_active=True).select_related('category')
    
    # Filtro por búsqueda
    search = request.GET.get('search', '')
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(sku__icontains=search)
        )
    
    # Filtro por categoría
    category_ids = request.GET.getlist('category')
    if category_ids:
        products = products.filter(category_id__in=category_ids)
    
    # Filtro por rango de precio
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Filtro por disponibilidad
    availability = request.GET.get('availability', '')
    if availability == 'in_stock':
        products = products.filter(stock_quantity__gt=0)
    
    # Ordenamiento
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Paginación manual (12 por página)
    from django.core.paginator import Paginator
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Categorías para filtros
    categories = Category.objects.filter(is_active=True).order_by('name')

    # Parámetros de filtro para links de paginación
    filter_parts = []
    if search:
        filter_parts.append(f'search={search}')
    for cat in category_ids:
        filter_parts.append(f'category={cat}')
    if min_price:
        filter_parts.append(f'min_price={min_price}')
    if max_price:
        filter_parts.append(f'max_price={max_price}')
    if availability:
        filter_parts.append(f'availability={availability}')
    if sort_by and sort_by != 'newest':
        filter_parts.append(f'sort={sort_by}')
    filter_params = ('&' + '&'.join(filter_parts)) if filter_parts else ''

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search': search,
        'selected_categories': category_ids,
        'min_price': min_price,
        'max_price': max_price,
        'availability': availability,
        'sort_by': sort_by,
        'filter_params': filter_params,
    }
    
    return render(request, 'store/catalog.html', context)


def product_detail(request, slug):
    """Detalle de producto"""
    # Asegurar que la sesión existe para el carrito anónimo
    if not request.session.session_key:
        request.session.create()
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Productos relacionados (misma categoría)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True,
        stock_quantity__gt=0
    ).exclude(id=product.id).order_by('-created_at')[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'store/product_detail.html', context)


def cart_view(request):
    """Vista del carrito"""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    
    # Calcular totales
    subtotal = sum(item.subtotal for item in items)
    
    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
    }
    
    return render(request, 'store/cart.html', context)


@require_POST
def cart_add(request):
    """Agregar producto al carrito (AJAX)"""
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Validar stock
        if product.stock_quantity < quantity:
            return JsonResponse({
                'success': False,
                'error': f'Solo hay {product.stock_quantity} unidades disponibles'
            })
        
        cart = get_or_create_cart(request)
        
        # Verificar si el producto ya está en el carrito
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Actualizar cantidad
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock_quantity:
                return JsonResponse({
                    'success': False,
                    'error': f'Solo hay {product.stock_quantity} unidades disponibles'
                })
            cart_item.quantity = new_quantity
            cart_item.save()
        
        # Contar items en el carrito
        cart_count = sum(item.quantity for item in cart.items.all())
        
        return JsonResponse({
            'success': True,
            'message': 'Producto agregado al carrito',
            'cart_count': cart_count
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def cart_update(request):
    """Actualizar cantidad en el carrito (AJAX)"""
    try:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        # Validar stock
        if quantity > cart_item.product.stock_quantity:
            return JsonResponse({
                'success': False,
                'error': f'Solo hay {cart_item.product.stock_quantity} unidades disponibles'
            })
        
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        # Calcular nuevos totales
        items = cart.items.select_related('product').all()
        subtotal = sum(item.subtotal for item in items)
        cart_count = sum(item.quantity for item in items)
        
        return JsonResponse({
            'success': True,
            'subtotal': float(subtotal),
            'item_subtotal': float(cart_item.subtotal) if quantity > 0 else 0,
            'cart_count': cart_count
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def cart_remove(request):
    """Eliminar producto del carrito (AJAX)"""
    try:
        item_id = request.POST.get('item_id')
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        # Calcular nuevos totales
        items = cart.items.select_related('product').all()
        subtotal = sum(item.subtotal for item in items)
        cart_count = sum(item.quantity for item in items)
        
        return JsonResponse({
            'success': True,
            'subtotal': float(subtotal),
            'cart_count': cart_count
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def cart_count(request):
    """Obtener cantidad de items en el carrito (AJAX)"""
    cart = get_or_create_cart(request)
    cart_count = sum(item.quantity for item in cart.items.all())
    
    return JsonResponse({
        'cart_count': cart_count
    })



# ============================================
# CUSTOMER AUTHENTICATION VIEWS
# ============================================

def customer_register(request):
    """Registro de nuevo cliente"""
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            # Crear cliente
            customer = Customer(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', ''),
            )
            customer.set_password(form.cleaned_data['password'])
            customer.save()
            
            # Enviar email de bienvenida
            try:
                send_mail(
                    subject=f'¡Bienvenido/a a Ross Crafts, {customer.first_name}!',
                    message=f'''
Hola {customer.first_name},

¡Gracias por registrarte en Ross Crafts!

Ahora puedes disfrutar de todas las ventajas de ser parte de nuestra comunidad:
- Realizar compras online de forma rápida y segura
- Ver el historial de tus pedidos
- Guardar tus direcciones de envío
- Recibir ofertas exclusivas

Visita nuestra tienda y descubre nuestros productos artesanales.

¡Bienvenido/a!
El equipo de Ross Crafts
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[customer.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error enviando email: {e}")
            
            # Iniciar sesión automáticamente
            customer.last_login = timezone.now()
            customer.save()
            auth_login(request, customer, backend='apps.ecommerce.backends.CustomerAuthBackend')
            
            messages.success(request, f'¡Bienvenido/a {customer.first_name}! Tu cuenta ha sido creada exitosamente.')
            
            # Redirigir según origen
            next_url = request.GET.get('next', '')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('ecommerce:catalog')
    else:
        form = CustomerRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'store/auth/register.html', context)


def customer_login(request):
    """Inicio de sesión de cliente"""
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Autenticar
            from apps.ecommerce.backends import CustomerAuthBackend
            backend = CustomerAuthBackend()
            customer = backend.authenticate(request, email=email, password=password)
            
            if customer:
                # Actualizar last_login
                customer.last_login = timezone.now()
                customer.save()
                
                # Iniciar sesión
                auth_login(request, customer, backend='apps.ecommerce.backends.CustomerAuthBackend')
                
                # Configurar duración de sesión
                if remember_me:
                    request.session.set_expiry(2592000)  # 30 días
                else:
                    request.session.set_expiry(0)  # Hasta cerrar navegador
                
                # Migrar carrito de sesión a cliente
                if request.session.session_key:
                    try:
                        session_cart = Cart.objects.filter(
                            session_key=request.session.session_key,
                            customer__isnull=True
                        ).order_by('-created_at').first()
                        if session_cart:
                            customer_cart, _ = Cart.objects.get_or_create(customer=customer, session_key='')
                            for item in session_cart.items.all():
                                existing = customer_cart.items.filter(product=item.product).first()
                                if existing:
                                    existing.quantity += item.quantity
                                    existing.save()
                                else:
                                    item.cart = customer_cart
                                    item.save()
                            session_cart.delete()
                    except Exception as e:
                        print(f"Error migrando carrito: {e}")
                
                messages.success(request, f'¡Bienvenido/a de nuevo, {customer.first_name}!')
                
                # Redirigir según origen
                next_url = request.GET.get('next', '')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('ecommerce:customer_profile')
            else:
                messages.error(request, 'Email o contraseña incorrectos.')
    else:
        form = CustomerLoginForm()
    
    context = {
        'form': form,
    }
    return render(request, 'store/auth/login.html', context)


def customer_logout(request):
    """Cerrar sesión de cliente"""
    if request.user.is_authenticated and isinstance(request.user, Customer):
        customer_name = request.user.first_name
        auth_logout(request)
        messages.success(request, f'Hasta pronto, {customer_name}!')
    
    return redirect('ecommerce:home')


@customer_login_required
def customer_profile(request):
    """Perfil del cliente"""
    customer = request.user
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('ecommerce:customer_profile')
    else:
        form = CustomerProfileForm(instance=customer)
    
    # Obtener estadísticas
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    sales = Sale.objects.filter(customer=customer).order_by('-created_at')
    
    # Calcular totales
    total_orders = orders.count()
    total_sales = sales.count()
    total_spent_orders = orders.aggregate(total=Sum('total'))['total'] or 0
    total_spent_sales = sales.aggregate(total=Sum('total'))['total'] or 0
    total_spent = total_spent_orders + total_spent_sales
    
    # Última compra
    last_order = orders.first()
    last_sale = sales.first()
    
    if last_order and last_sale:
        last_purchase = last_order if last_order.created_at > last_sale.created_at else last_sale
    elif last_order:
        last_purchase = last_order
    elif last_sale:
        last_purchase = last_sale
    else:
        last_purchase = None
    
    context = {
        'form': form,
        'customer': customer,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'total_transactions': total_orders + total_sales,
        'total_spent': total_spent,
        'last_purchase': last_purchase,
    }
    return render(request, 'store/account/profile.html', context)


@customer_login_required
def customer_orders(request):
    """Historial de pedidos del cliente"""
    customer = request.user
    
    # Obtener pedidos online y ventas presenciales
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    sales = Sale.objects.filter(customer=customer).order_by('-created_at')
    
    context = {
        'customer': customer,
        'orders': orders,
        'sales': sales,
    }
    return render(request, 'store/account/orders.html', context)


@customer_login_required
def customer_order_detail(request, pk):
    """Detalle de un pedido"""
    customer = request.user
    order = get_object_or_404(Order, pk=pk, customer=customer)
    
    # Obtener items del pedido a través de la venta asociada
    items = []
    if order.sale:
        items = order.sale.items.select_related('product').all()
    
    context = {
        'customer': customer,
        'order': order,
        'items': items,
    }
    return render(request, 'store/account/order_detail.html', context)

@customer_login_required
def customer_change_password(request):
    """Cambio de contraseña"""
    customer = request.user
    
    if request.method == 'POST':
        form = CustomerChangePasswordForm(customer, request.POST)
        if form.is_valid():
            customer.set_password(form.cleaned_data['new_password'])
            customer.save()
            
            # Mantener sesión activa
            auth_login(request, customer, backend='apps.ecommerce.backends.CustomerAuthBackend')
            
            messages.success(request, 'Contraseña actualizada exitosamente.')
            return redirect('ecommerce:customer_profile')
    else:
        form = CustomerChangePasswordForm(customer)
    
    context = {
        'form': form,
        'customer': customer,
    }
    return render(request, 'store/account/change_password.html', context)


def customer_password_reset(request):
    """Solicitar reset de contraseña"""
    if request.method == 'POST':
        form = CustomerPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                customer = Customer.objects.get(email=email, is_active=True)
                
                # Generar token (simplificado - en producción usar tokens seguros)
                from django.contrib.auth.tokens import default_token_generator
                from django.utils.http import urlsafe_base64_encode
                from django.utils.encoding import force_bytes
                
                token = default_token_generator.make_token(customer)
                uid = urlsafe_base64_encode(force_bytes(customer.pk))
                
                # Enviar email
                reset_url = request.build_absolute_uri(
                    f'/cuenta/reset/{uid}/{token}/'
                )
                
                send_mail(
                    subject='Recuperación de contraseña - Ross Crafts',
                    message=f'''
Hola {customer.first_name},

Recibimos una solicitud para restablecer tu contraseña.

Haz clic en el siguiente enlace para crear una nueva contraseña:
{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este mensaje.

Saludos,
El equipo de Ross Crafts
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[customer.email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Te hemos enviado un email con instrucciones para restablecer tu contraseña.')
                return redirect('ecommerce:customer_login')
            
            except Customer.DoesNotExist:
                # No revelar si el email existe o no
                messages.success(request, 'Si el email existe en nuestro sistema, recibirás instrucciones para restablecer tu contraseña.')
                return redirect('ecommerce:customer_login')
            except Exception as e:
                messages.error(request, 'Hubo un error al enviar el email. Por favor intenta nuevamente.')
    else:
        form = CustomerPasswordResetForm()
    
    context = {
        'form': form,
    }
    return render(request, 'store/auth/password_reset.html', context)


def customer_password_reset_confirm(request, uidb64, token):
    """Confirmar nueva contraseña"""
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        customer = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        customer = None
    
    if customer and default_token_generator.check_token(customer, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if password and password == password_confirm and len(password) >= 8:
                customer.set_password(password)
                customer.save()
                
                messages.success(request, 'Contraseña restablecida exitosamente. Ya puedes iniciar sesión.')
                return redirect('ecommerce:customer_login')
            else:
                messages.error(request, 'Las contraseñas no coinciden o son muy cortas (mínimo 8 caracteres).')
        
        context = {
            'validlink': True,
            'uidb64': uidb64,
            'token': token,
        }
        return render(request, 'store/auth/password_reset_confirm.html', context)
    else:
        messages.error(request, 'El enlace de recuperación es inválido o ha expirado.')
        return redirect('ecommerce:customer_password_reset')
