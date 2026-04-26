# Guía de Uso - Sistema de Clientes Ross Crafts

## Índice
1. [Registro de Clientes](#registro-de-clientes)
2. [Inicio de Sesión](#inicio-de-sesión)
3. [Gestión de Perfil](#gestión-de-perfil)
4. [Historial de Pedidos](#historial-de-pedidos)
5. [Recuperación de Contraseña](#recuperación-de-contraseña)
6. [Administración](#administración)

---

## Registro de Clientes

### URL: `/cuenta/registro/`

### Proceso de Registro
1. Acceder a la página de registro
2. Completar el formulario:
   - **Nombre** (requerido)
   - **Apellido** (requerido)
   - **Email** (requerido, único)
   - **Teléfono** (opcional)
   - **Contraseña** (mínimo 8 caracteres, al menos 1 número)
   - **Confirmar Contraseña** (debe coincidir)
3. Hacer clic en "Crear Cuenta"

### Después del Registro
- Se envía un email de bienvenida automáticamente
- El cliente inicia sesión automáticamente
- Redirige a la tienda o al checkout (si venía del carrito)

### Validaciones
- ✅ Email único (no puede estar registrado previamente)
- ✅ Contraseña mínimo 8 caracteres
- ✅ Contraseña debe contener al menos un número
- ✅ Las contraseñas deben coincidir

---

## Inicio de Sesión

### URL: `/cuenta/login/`

### Proceso de Login
1. Acceder a la página de inicio de sesión
2. Ingresar:
   - **Email** (registrado en el sistema)
   - **Contraseña**
   - **Recordarme** (opcional, mantiene sesión por 30 días)
3. Hacer clic en "Iniciar Sesión"

### Después del Login
- Migración automática del carrito de sesión al cliente
- Redirige a la página solicitada (`?next=`) o al perfil
- Mensaje de bienvenida personalizado

### Duración de Sesión
- **Con "Recordarme"**: 30 días
- **Sin "Recordarme"**: Hasta cerrar el navegador

### Migración de Carrito
Al iniciar sesión, los productos del carrito anónimo se transfieren automáticamente:
- Si el producto ya existe en el carrito del cliente, se suman las cantidades
- Si es nuevo, se agrega al carrito del cliente
- El carrito de sesión se elimina

---

## Gestión de Perfil

### URL: `/cuenta/perfil/`

### Información Mostrada
1. **Resumen de Cuenta**:
   - Total de compras realizadas
   - Total gastado (S/.)
   - Fecha de última compra

2. **Datos Personales** (editables):
   - Nombre
   - Apellido
   - Teléfono
   - Dirección
   - Email (solo lectura)

### Editar Perfil
1. Modificar los campos deseados
2. Hacer clic en "Guardar Cambios"
3. Confirmación de actualización exitosa

### Navegación
Sidebar con acceso rápido a:
- Perfil
- Mis Pedidos
- Cambiar Contraseña
- Cerrar Sesión

---

## Historial de Pedidos

### URL: `/cuenta/mis-pedidos/`

### Información Mostrada

#### Pedidos Online
- N° de Pedido
- Fecha y hora
- Total (S/.)
- Estado (Pendiente, Pagado, Enviado, Entregado, Cancelado)
- Botón "Ver Detalle"

#### Compras Presenciales
- N° de Comprobante
- Fecha y hora
- Total (S/.)
- Método de pago
- Estado (Completado)

### Ver Detalle de Pedido

#### URL: `/cuenta/mis-pedidos/<id>/`

Muestra:
- Información del pedido (fecha, estado, total)
- Dirección de envío
- ID de pago (si existe)
- Lista de productos:
  - Nombre del producto
  - Precio unitario
  - Cantidad
  - Subtotal
- Total del pedido

---

## Recuperación de Contraseña

### Solicitar Reset

#### URL: `/cuenta/recuperar-contrasena/`

1. Ingresar el email registrado
2. Hacer clic en "Enviar Instrucciones"
3. Revisar el email (o consola en desarrollo)

### Email de Recuperación
- Asunto: "Recuperación de contraseña - Ross Crafts"
- Contiene enlace único que expira en 24 horas
- Formato: `/cuenta/reset/<uidb64>/<token>/`

### Confirmar Nueva Contraseña

#### URL: `/cuenta/reset/<uidb64>/<token>/`

1. Hacer clic en el enlace del email
2. Ingresar nueva contraseña (mínimo 8 caracteres)
3. Confirmar nueva contraseña
4. Hacer clic en "Restablecer Contraseña"
5. Redirige al login

### Seguridad
- El enlace expira en 24 horas
- El token es de un solo uso
- No se revela si el email existe en el sistema

---

## Cambiar Contraseña

### URL: `/cuenta/cambiar-contrasena/`

### Proceso
1. Ingresar contraseña actual
2. Ingresar nueva contraseña (mínimo 8 caracteres, al menos 1 número)
3. Confirmar nueva contraseña
4. Hacer clic en "Cambiar Contraseña"

### Validaciones
- ✅ Contraseña actual correcta
- ✅ Nueva contraseña cumple requisitos
- ✅ Las contraseñas coinciden

### Después del Cambio
- La sesión se mantiene activa (no requiere login nuevamente)
- Mensaje de confirmación
- Redirige al perfil

---

## Administración

### Crear Cliente Manualmente (Django Shell)

```python
python manage.py shell

from apps.customers.models import Customer

# Crear cliente
customer = Customer(
    first_name='Juan',
    last_name='Pérez',
    email='juan@example.com',
    phone='987654321',
    address='Av. Principal 123'
)
customer.set_password('MiPassword123')
customer.save()

print(f"Cliente creado: {customer.full_name}")
```

### Verificar Contraseña

```python
from apps.customers.models import Customer

customer = Customer.objects.get(email='juan@example.com')

# Verificar contraseña
if customer.check_password('MiPassword123'):
    print("Contraseña correcta")
else:
    print("Contraseña incorrecta")
```

### Cambiar Contraseña Manualmente

```python
from apps.customers.models import Customer

customer = Customer.objects.get(email='juan@example.com')
customer.set_password('NuevaPassword123')
customer.save()

print("Contraseña actualizada")
```

### Desactivar Cliente

```python
from apps.customers.models import Customer

customer = Customer.objects.get(email='juan@example.com')
customer.is_active = False
customer.save()

print("Cliente desactivado")
```

### Listar Clientes Activos

```python
from apps.customers.models import Customer

clientes = Customer.objects.filter(is_active=True).order_by('-created_at')

for cliente in clientes:
    print(f"{cliente.full_name} - {cliente.email}")
```

---

## Integración con Carrito

### Carrito Anónimo
- Se crea automáticamente usando `session_key`
- Persiste mientras la sesión esté activa
- Se migra al cliente al iniciar sesión

### Carrito de Cliente Autenticado
- Se vincula al cliente mediante `customer` ForeignKey
- Persiste entre sesiones
- Se mantiene tras cerrar sesión y volver a iniciar

### Función get_or_create_cart()

```python
def get_or_create_cart(request):
    """Obtener o crear carrito para el usuario/sesión"""
    if request.user.is_authenticated and isinstance(request.user, Customer):
        # Usuario autenticado con perfil de cliente
        cart, created = Cart.objects.get_or_create(customer=request.user)
    else:
        # Usuario anónimo - usar sesión
        if not request.session.session_key:
            request.session.create()
        
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    return cart
```

---

## Emails

### Configuración de Desarrollo
Los emails se muestran en la consola:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Configuración de Producción
Usar SMTP real (ejemplo con Gmail):

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicación'
DEFAULT_FROM_EMAIL = 'Ross Crafts <noreply@rosscrafts.com>'
```

### Tipos de Emails
1. **Bienvenida**: Tras registro exitoso
2. **Recuperación de contraseña**: Con enlace de reset

---

## Seguridad

### Separación de Sistemas
- **Staff**: Usa `django.contrib.auth.backends.ModelBackend`
- **Clientes**: Usa `apps.ecommerce.backends.CustomerAuthBackend`
- No hay cruce entre sistemas

### Contraseñas
- Hasheadas con `make_password()` de Django
- Algoritmo: PBKDF2 con SHA256
- Nunca se almacenan en texto plano

### Tokens de Reset
- Generados con `default_token_generator`
- Expiran en 24 horas
- Un solo uso

### Decorador @customer_login_required
Protege vistas que requieren autenticación de cliente:
- Verifica que el usuario esté autenticado
- Verifica que sea instancia de Customer (no staff)
- Redirige a login si no cumple

---

## Solución de Problemas

### "Email ya está registrado"
- El email debe ser único en el sistema
- Usar la opción "¿Olvidaste tu contraseña?" si ya tienes cuenta

### "Contraseña incorrecta"
- Verificar mayúsculas/minúsculas
- Usar "¿Olvidaste tu contraseña?" para resetear

### "El enlace de recuperación es inválido"
- El enlace expira en 24 horas
- Solicitar un nuevo enlace de recuperación

### "Esta área es solo para clientes"
- Estás intentando acceder con una cuenta de staff
- Cerrar sesión e iniciar con cuenta de cliente

### Carrito no se migra
- Verificar que la sesión esté activa
- Limpiar cookies del navegador
- Intentar agregar productos nuevamente

---

## Próximas Funcionalidades

### En Desarrollo
- ✅ Sistema de autenticación completo
- ✅ Gestión de perfil
- ✅ Historial de pedidos
- ⏳ Checkout y pagos con Stripe
- ⏳ Notificaciones por email
- ⏳ Verificación de email

### Futuras Mejoras
- Direcciones guardadas
- Lista de deseos
- Reseñas de productos
- Programa de puntos/recompensas
- Notificaciones push

---

## Soporte

Para problemas o consultas:
- Email: soporte@rosscrafts.com
- Teléfono: (01) 234-5678
- Horario: Lunes a Viernes, 9:00 AM - 6:00 PM

---

**Última actualización**: 25 de abril de 2026
**Versión**: 1.0.0
