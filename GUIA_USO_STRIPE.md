# Guía de Uso - Sistema de Pagos con Stripe

## Configuración Inicial

### 1. Obtener Claves de Stripe

1. Crear cuenta en [Stripe](https://stripe.com)
2. Ir a **Developers** → **API keys**
3. Copiar las claves de prueba:
   - **Publishable key** (empieza con `pk_test_`)
   - **Secret key** (empieza con `sk_test_`)

### 2. Configurar Variables de Entorno

Editar `.env`:
```env
STRIPE_PUBLIC_KEY=pk_test_tu_clave_publica
STRIPE_SECRET_KEY=sk_test_tu_clave_secreta
STRIPE_WEBHOOK_SECRET=whsec_tu_webhook_secret
```

### 3. Configurar Webhook (Opcional para Testing Local)

#### Opción A: Stripe CLI (Recomendado para desarrollo)

```bash
# Instalar Stripe CLI
# Windows: scoop install stripe
# Mac: brew install stripe/stripe-cli/stripe
# Linux: Ver https://stripe.com/docs/stripe-cli

# Login
stripe login

# Forward webhooks a localhost
stripe listen --forward-to localhost:8000/stripe/webhook/

# Copiar el webhook secret que aparece
# Agregarlo a .env como STRIPE_WEBHOOK_SECRET
```

#### Opción B: Dashboard de Stripe (Para producción)

1. Ir a **Developers** → **Webhooks**
2. Hacer clic en **Add endpoint**
3. URL: `https://tu-dominio.com/stripe/webhook/`
4. Eventos: `payment_intent.succeeded`
5. Copiar **Signing secret** y agregarlo a `.env`

---

## Flujo de Compra para Clientes

### Paso 1: Agregar Productos al Carrito

1. Navegar a `/tienda/`
2. Hacer clic en productos para ver detalles
3. Agregar productos al carrito
4. Ir a `/carrito/` para revisar

### Paso 2: Iniciar Checkout

1. Hacer clic en "Proceder al Checkout"
2. Redirige a `/checkout/`

### Paso 3: Datos de Envío

**Formulario:**
- Nombre completo
- Dirección de envío
- Distrito, Ciudad, Departamento
- Teléfono
- Email

**Nota:** Si el cliente está autenticado, los datos se pre-llenan automáticamente.

Hacer clic en "Continuar"

### Paso 4: Revisar Pedido

**Se muestra:**
- Dirección de envío confirmada
- Lista de productos con cantidades
- Subtotal
- Costo de envío (S/. 10.00 o Gratis si total > S/. 150)
- Total a pagar

Hacer clic en "Proceder al Pago"

### Paso 5: Ingresar Datos de Tarjeta

**Tarjetas de Prueba (Modo Desarrollo):**

✅ **Pago exitoso:**
```
Número: 4242 4242 4242 4242
Vencimiento: 12/25 (cualquier fecha futura)
CVV: 123 (cualquier 3 dígitos)
```

❌ **Tarjeta rechazada:**
```
Número: 4000 0000 0000 0002
Vencimiento: 12/25
CVV: 123
```

🔐 **Requiere 3D Secure:**
```
Número: 4000 0025 0000 3155
Vencimiento: 12/25
CVV: 123
```

Hacer clic en "Pagar S/. XX.XX"

### Paso 6: Confirmación

- Redirige a `/checkout/exitoso/`
- Muestra número de pedido
- Email de confirmación enviado
- Opciones: "Ver mis pedidos" o "Seguir comprando"

---

## Para Administradores

### Ver Pedidos Procesados

1. Ir a Django Admin: `/admin/`
2. **Ecommerce** → **Orders**
3. Ver pedidos con `payment_intent_id` de Stripe

### Ver Ventas Generadas

1. Django Admin → **Sales** → **Sales**
2. Filtrar por `payment_method = 'online'`
3. Ver `receipt_number` generado (RC-YYYY-XXXXXX)

### Ver Pagos en Stripe

1. Ir a [Dashboard de Stripe](https://dashboard.stripe.com)
2. **Payments** → Ver todos los pagos
3. Hacer clic en un pago para ver detalles
4. Ver metadata con información del pedido

### Verificar Stock

1. Django Admin → **Stock** → **Products**
2. Verificar que `stock_quantity` se decrementó
3. Ver **Stock Movements** para historial

---

## Solución de Problemas

### "Tu tarjeta fue rechazada"

**Causas comunes:**
- Usando tarjeta real en modo de prueba
- Número de tarjeta incorrecto
- Tarjeta de prueba para rechazo (4000 0000 0000 0002)

**Solución:**
- Usar tarjeta de prueba: 4242 4242 4242 4242
- Verificar que estás en modo de prueba
- Revisar fecha de vencimiento y CVV

### "Tu carrito está vacío"

**Causa:**
- Carrito fue vaciado o expiró la sesión

**Solución:**
- Agregar productos nuevamente al carrito
- Verificar que las cookies estén habilitadas

### "Por favor completa los datos de envío"

**Causa:**
- Intentando acceder a `/checkout/pago/` directamente
- Sesión expiró

**Solución:**
- Volver a `/checkout/` y completar paso 1

### Webhook no funciona

**Síntomas:**
- Pago exitoso pero no se crea el pedido
- No se envía email de confirmación

**Solución:**

1. **Verificar Stripe CLI está corriendo:**
   ```bash
   stripe listen --forward-to localhost:8000/stripe/webhook/
   ```

2. **Verificar STRIPE_WEBHOOK_SECRET en .env:**
   - Debe coincidir con el secret del CLI o Dashboard

3. **Ver logs del webhook:**
   ```bash
   stripe logs tail
   ```

4. **Verificar en Django:**
   - Ver logs en consola
   - Verificar que la URL `/stripe/webhook/` es accesible

### Email no se envía

**Causa:**
- `EMAIL_BACKEND` configurado para consola

**Solución:**
- En desarrollo: Ver email en la consola del servidor
- En producción: Configurar SMTP real en `settings.py`

---

## Testing Completo

### Escenario 1: Compra Exitosa

```bash
# 1. Iniciar servidor
python manage.py runserver

# 2. Iniciar Stripe CLI (otra terminal)
stripe listen --forward-to localhost:8000/stripe/webhook/

# 3. Navegar a la tienda
http://localhost:8000/tienda/

# 4. Agregar productos al carrito

# 5. Ir a checkout
http://localhost:8000/checkout/

# 6. Completar datos de envío
Nombre: Juan Pérez
Dirección: Av. Principal 123
Distrito: Miraflores
Ciudad: Lima
Departamento: Lima
Teléfono: 987654321
Email: juan@test.com

# 7. Revisar resumen y continuar

# 8. Ingresar tarjeta de prueba
4242 4242 4242 4242
12/25
123

# 9. Hacer clic en "Pagar"

# 10. Verificar:
- Redirige a /checkout/exitoso/
- Email en consola
- Pedido en /cuenta/mis-pedidos/ (si autenticado)
- Stock decrementado
- Venta creada en admin
```

### Escenario 2: Tarjeta Rechazada

```bash
# Seguir pasos 1-7 del Escenario 1

# 8. Ingresar tarjeta de rechazo
4000 0000 0000 0002
12/25
123

# 9. Hacer clic en "Pagar"

# 10. Verificar:
- Mensaje de error: "Tu tarjeta fue rechazada..."
- No se crea pedido
- Stock no cambia
- Puede reintentar con otra tarjeta
```

### Escenario 3: Cancelación

```bash
# Seguir pasos 1-7 del Escenario 1

# 8. Cerrar la ventana o navegar a otra página

# 9. Ir a /checkout/cancelado/

# 10. Verificar:
- Mensaje de cancelación
- Botones para reintentar o volver al carrito
- No se crea pedido
```

---

## Monitoreo en Producción

### Dashboard de Stripe

1. **Payments**: Ver todos los pagos procesados
2. **Customers**: Ver clientes (si se crean en Stripe)
3. **Logs**: Ver eventos y webhooks
4. **Disputes**: Gestionar disputas/chargebacks

### Métricas Importantes

- **Tasa de éxito de pagos**: % de pagos exitosos vs fallidos
- **Valor promedio de pedido**: Total / N° de pedidos
- **Tiempo de procesamiento**: Desde inicio hasta confirmación
- **Tasa de abandono**: % de carritos no completados

### Alertas Recomendadas

- Webhook fallando (> 5 errores consecutivos)
- Tasa de rechazo alta (> 20%)
- Pedidos sin procesar (payment_intent sin Order)
- Stock agotado durante checkout

---

## Migración a Producción

### 1. Obtener Claves de Producción

1. Ir a Stripe Dashboard
2. Cambiar de "Test mode" a "Live mode"
3. Copiar claves de producción:
   - `pk_live_...`
   - `sk_live_...`

### 2. Actualizar .env

```env
STRIPE_PUBLIC_KEY=pk_live_tu_clave_publica
STRIPE_SECRET_KEY=sk_live_tu_clave_secreta
STRIPE_WEBHOOK_SECRET=whsec_tu_webhook_secret_produccion
```

### 3. Configurar Webhook en Producción

1. Stripe Dashboard → **Webhooks**
2. Add endpoint: `https://tu-dominio.com/stripe/webhook/`
3. Eventos: `payment_intent.succeeded`
4. Copiar signing secret a `.env`

### 4. Configurar HTTPS

**Stripe requiere HTTPS en producción**

- Usar certificado SSL (Let's Encrypt, Cloudflare, etc.)
- Configurar servidor web (Nginx, Apache)
- Verificar que todas las URLs usen `https://`

### 5. Configurar Email SMTP

```python
# settings/production.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
```

### 6. Testing en Producción

1. Hacer una compra de prueba con tarjeta real
2. Verificar webhook funciona
3. Verificar email se envía
4. Verificar pedido se crea
5. Hacer reembolso de prueba

---

## Preguntas Frecuentes

### ¿Cuánto cobra Stripe?

**Perú:**
- 3.95% + S/. 1.00 por transacción exitosa
- Sin costos de setup o mensuales
- Ver [precios actualizados](https://stripe.com/pe/pricing)

### ¿Qué monedas soporta?

- Configurado para PEN (Soles peruanos)
- Stripe soporta 135+ monedas
- Cambiar `currency='pen'` en `create_payment_intent()`

### ¿Cómo hacer reembolsos?

```python
# En Django shell o vista de admin
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Reembolso completo
stripe.Refund.create(payment_intent='pi_xxx')

# Reembolso parcial
stripe.Refund.create(
    payment_intent='pi_xxx',
    amount=5000  # S/. 50.00 en centavos
)
```

### ¿Cómo guardar tarjetas de clientes?

Requiere implementar:
1. Stripe Customer API
2. Payment Methods
3. Setup Intents para guardar tarjetas
4. PCI compliance adicional

**No implementado actualmente** - cada pago requiere ingresar tarjeta.

### ¿Soporta pagos recurrentes/suscripciones?

No actualmente. Requiere:
- Stripe Subscriptions API
- Billing portal
- Gestión de planes

### ¿Qué pasa si el webhook falla?

- Stripe reintenta automáticamente
- Hasta 3 días de reintentos
- Ver logs en Dashboard → Webhooks
- Implementar idempotencia (ya hecho)

---

## Recursos Adicionales

### Documentación Oficial

- [Stripe Docs](https://stripe.com/docs)
- [Payment Intents API](https://stripe.com/docs/payments/payment-intents)
- [Webhooks](https://stripe.com/docs/webhooks)
- [Testing](https://stripe.com/docs/testing)

### Herramientas

- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Stripe Dashboard](https://dashboard.stripe.com)
- [API Reference](https://stripe.com/docs/api)

### Soporte

- [Stripe Support](https://support.stripe.com)
- [Community Forum](https://stripe.com/community)
- [Status Page](https://status.stripe.com)

---

**Última actualización**: 25 de abril de 2026
**Versión**: 1.0.0
