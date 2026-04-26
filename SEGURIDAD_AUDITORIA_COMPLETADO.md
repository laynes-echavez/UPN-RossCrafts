# 🔒 SEGURIDAD Y AUDITORÍA - ROSS CRAFTS

## ✅ IMPLEMENTACIÓN COMPLETADA

### 1. MIDDLEWARE DE AUDITORÍA

**Ubicación:** `apps/audit/middleware.py`

**Características:**
- ✅ Registra automáticamente todas las acciones en áreas administrativas
- ✅ Excluye rutas públicas (tienda, carrito, webhooks, estáticos)
- ✅ Captura: usuario, método HTTP, URL, IP, código de respuesta
- ✅ Manejo de proxies (X-Forwarded-For)
- ✅ No interrumpe el flujo si falla el registro

**URLs Auditadas:**
- `/dashboard/*` - Panel administrativo
- `/stock/*` - Gestión de inventario
- `/ventas/*` - Punto de venta
- `/clientes/*` - Gestión de clientes
- `/proveedores/*` - Gestión de proveedores
- `/reportes/*` - Reportes y estadísticas
- `/admin/*` - Django Admin

**URLs NO Auditadas:**
- `/tienda/*` - Tienda pública
- `/carrito/*` - Carrito de compras
- `/cuenta/*` - Cuenta de cliente
- `/static/*` - Archivos estáticos
- `/media/*` - Archivos multimedia
- `/stripe/webhook/*` - Webhooks de Stripe
- `/checkout/*` - Proceso de pago
- `/payment/*` - Formulario de pago

---

### 2. SISTEMA DE LOGGING

**Ubicación:** `settings/base.py`

**Configuración:**
```python
LOGGING = {
    'formatters': {
        'detailed': '{asctime} | {levelname} | {module} | {message}'
    },
    'handlers': {
        'error_file': 'logs/errors.log',      # Errores críticos
        'warning_file': 'logs/warnings.log',  # Advertencias
        'activity_file': 'logs/activity.log', # Actividad del sistema
    },
    'loggers': {
        'apps.sales': INFO level,     # Registra todas las ventas
        'apps.payments': INFO level,  # Registra todos los pagos
        'django': WARNING level,      # Errores y advertencias de Django
    }
}
```

**Archivos de Log:**
- `logs/errors.log` - Errores críticos del sistema
- `logs/warnings.log` - Advertencias y problemas menores
- `logs/activity.log` - Actividad de ventas y pagos
- `logs/django.log` - Log general de Django (legacy)

**Ejemplos de Uso:**

```python
# En apps/sales/views.py
logger.info(
    f"Venta #{sale.id} registrada por {request.user.username} | "
    f"Total: S/. {sale.total:.2f} | Cliente: {customer_name}"
)

# En apps/payments/views.py
logger.info(
    f"Pago Stripe exitoso | Order #{order.id} | Sale #{sale.id} | "
    f"Total: S/. {total:.2f} | Cliente: {customer_email}"
)

logger.warning(
    f"Intento de webhook Stripe con firma inválida desde {ip_address}"
)

logger.error(
    f"Error procesando webhook Stripe: {str(e)}"
)
```

---

### 3. VISTA DE AUDITORÍA

**URL:** `/dashboard/auditoria/`

**Acceso:** Solo usuarios con rol `gerente`

**Características:**
- ✅ Tabla con últimas 500 entradas
- ✅ Paginación de 25 registros por página
- ✅ Ordenamiento explícito por timestamp (compatible con SQL Server)
- ✅ Filtros disponibles:
  - Usuario (dropdown con todos los usuarios staff)
  - Método HTTP (GET, POST, PUT, DELETE, LOGIN, LOGOUT)
  - Rango de fechas (desde/hasta)
- ✅ Exportación a Excel con los filtros aplicados
- ✅ Información mostrada:
  - Fecha/Hora
  - Usuario y Rol
  - Método HTTP (con badges de colores)
  - URL (truncada a 60 caracteres)
  - Dirección IP
  - Código HTTP (con badges de colores)

**Exportación a Excel:**
- URL: `/dashboard/auditoria/export/`
- Formato: `.xlsx` con estilos profesionales
- Nombre: `auditoria_YYYYMMDD_HHMMSS.xlsx`
- Incluye: todos los filtros aplicados en la vista
- Límite: 500 registros más recientes

---

### 4. RATE LIMITING EN LOGIN

**Ubicación:** `apps/authentication/views.py`

**Configuración:**
```python
@ratelimit(key='ip', rate='5/15m', method='POST', block=True)
def login_view(request):
    ...
```

**Características:**
- ✅ Máximo 5 intentos de login por IP cada 15 minutos
- ✅ Bloqueo automático después de exceder el límite
- ✅ Registro de intentos fallidos en AuditLog
- ✅ Registro de logins exitosos en AuditLog

**Mensaje de Error:**
```
"Has realizado demasiados intentos. Por favor espera 15 minutos."
```

**Dependencia:**
```bash
pip install django-ratelimit
```

---

### 5. CONFIGURACIONES DE SEGURIDAD

**Ubicación:** `settings/base.py`

**Configuraciones Aplicadas:**

```python
# Protección XSS
SECURE_BROWSER_XSS_FILTER = True

# Protección contra clickjacking
X_FRAME_OPTIONS = 'DENY'

# Protección contra MIME sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Cookies seguras
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
```

**Configuraciones de Producción:**

En `settings/production.py`:
```python
# Forzar HTTPS
SECURE_SSL_REDIRECT = True

# Cookies solo por HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SQL Server con certificado válido
DATABASES['default']['OPTIONS']['TrustServerCertificate'] = 'no'
```

---

### 6. SEGURIDAD EN STRIPE WEBHOOK

**Ubicación:** `apps/payments/views.py`

**Verificación de Firma:**

```python
try:
    event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
except ValueError as e:
    # Payload inválido
    logger.error(f"Webhook con payload inválido desde {ip}: {str(e)}")
    return HttpResponse(status=400)
except stripe.error.SignatureVerificationError as e:
    # Firma inválida - CRÍTICO
    logger.warning(f"Intento de webhook con firma inválida desde {ip}: {str(e)}")
    return HttpResponse(status=400)
```

**Características:**
- ✅ Verificación obligatoria de firma HMAC
- ✅ Rechazo inmediato si la firma es inválida (status 400)
- ✅ Logging de intentos fallidos con IP del origen
- ✅ Nunca procesa el evento si la firma falla
- ✅ Protección contra replay attacks (idempotencia)

---

### 7. SEGURIDAD EN SQL SERVER

**Autenticación de Windows:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'Trusted_Connection': 'yes',  # Autenticación de Windows
            'TrustServerCertificate': 'yes',  # Solo en desarrollo
        },
    }
}
```

**Ventajas de Seguridad:**
- ✅ No se almacenan contraseñas en el código
- ✅ Autenticación integrada con Windows
- ✅ Credenciales gestionadas por el sistema operativo
- ✅ Auditoría de Windows disponible

**Recomendaciones:**
- ✅ `.env` en `.gitignore` (verificado)
- ✅ `DB_HOST` y `DB_NAME` en variables de entorno
- ✅ En producción: usar `TrustServerCertificate=no` con certificado válido
- ✅ Usuario de Windows con permisos mínimos (no sysadmin)

**Permisos Recomendados en SQL Server:**
```sql
-- Crear usuario de Windows para la aplicación
CREATE LOGIN [DOMAIN\AppUser] FROM WINDOWS;
USE ross_crafts_db;
CREATE USER [DOMAIN\AppUser] FOR LOGIN [DOMAIN\AppUser];

-- Otorgar solo permisos necesarios
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO [DOMAIN\AppUser];
-- NO otorgar: sysadmin, db_owner, ALTER, DROP
```

---

### 8. VARIABLES DE ENTORNO

**Archivo:** `.env`

**Variables Críticas:**
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Base de datos
DB_NAME=ross_crafts_db
DB_HOST=YOUR-PC\SQLEXPRESS01

# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Verificación de Seguridad:**
```bash
# Verificar que .env está en .gitignore
cat .gitignore | grep .env

# Resultado esperado:
# .env
```

---

## 📋 CHECKLIST DE SEGURIDAD

### Implementado ✅

- [x] Middleware de auditoría para áreas administrativas
- [x] Sistema de logging con múltiples niveles
- [x] Vista de auditoría con filtros y exportación
- [x] Rate limiting en login (5 intentos / 15 min)
- [x] Registro de intentos de login fallidos
- [x] Protección XSS, clickjacking, MIME sniffing
- [x] Cookies HttpOnly para sesión y CSRF
- [x] Verificación de firma en webhooks de Stripe
- [x] Logging de intentos de webhook inválidos
- [x] Autenticación de Windows para SQL Server
- [x] Variables de entorno para credenciales
- [x] Configuraciones de seguridad para producción
- [x] Logging de todas las ventas y pagos

### Para Producción 🚀

- [ ] Activar `SECURE_SSL_REDIRECT = True`
- [ ] Activar `SESSION_COOKIE_SECURE = True`
- [ ] Activar `CSRF_COOKIE_SECURE = True`
- [ ] Configurar certificado SSL válido
- [ ] Cambiar `TrustServerCertificate = no` en SQL Server
- [ ] Configurar usuario de Windows con permisos mínimos
- [ ] Configurar SMTP real para emails
- [ ] Configurar backup automático de logs
- [ ] Configurar rotación de logs
- [ ] Revisar y actualizar `ALLOWED_HOSTS`

---

## 🧪 PRUEBAS

### 1. Probar Middleware de Auditoría

```bash
# Iniciar servidor
python manage.py runserver

# Acceder a diferentes URLs del dashboard
# Verificar en la base de datos:
SELECT TOP 10 * FROM rc_audit_logs ORDER BY timestamp DESC;
```

### 2. Probar Rate Limiting

```bash
# Intentar login 6 veces con credenciales incorrectas
# El 6to intento debe mostrar mensaje de bloqueo
```

### 3. Probar Vista de Auditoría

```bash
# Acceder como gerente a:
http://localhost:8000/dashboard/auditoria/

# Probar filtros y exportación a Excel
```

### 4. Probar Logging

```bash
# Realizar una venta en el POS
# Verificar en logs/activity.log:
tail -f logs/activity.log

# Resultado esperado:
# 2026-04-25 10:30:45 | INFO | views | Venta #123 registrada por admin | Total: S/. 150.00 | Cliente: Juan Pérez
```

### 5. Probar Webhook de Stripe

```bash
# Usar Stripe CLI para simular webhook
stripe listen --forward-to localhost:8000/stripe/webhook/

# Simular pago exitoso
stripe trigger payment_intent.succeeded

# Verificar en logs/activity.log el registro del pago
```

---

## 📊 MODELO DE DATOS

### AuditLog

```python
class AuditLog(models.Model):
    user = ForeignKey(User)           # Usuario que realizó la acción
    action = CharField(max_length=10) # GET, POST, PUT, DELETE, LOGIN, LOGOUT
    url = CharField(max_length=500)   # URL accedida
    ip_address = CharField(max_length=45)  # IPv4 o IPv6
    status_code = IntegerField()      # Código HTTP de respuesta
    timestamp = DateTimeField()       # Fecha y hora de la acción
```

---

## 🔧 MANTENIMIENTO

### Limpieza de Logs Antiguos

```python
# Script para limpiar logs de más de 90 días
from datetime import timedelta
from django.utils import timezone
from apps.audit.models import AuditLog

cutoff_date = timezone.now() - timedelta(days=90)
deleted = AuditLog.objects.filter(timestamp__lt=cutoff_date).delete()
print(f"Eliminados {deleted[0]} registros antiguos")
```

### Rotación de Archivos de Log

Agregar en `settings/base.py`:

```python
'handlers': {
    'activity_file': {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': BASE_DIR / 'logs/activity.log',
        'maxBytes': 10485760,  # 10MB
        'backupCount': 5,
        'formatter': 'detailed',
    },
}
```

---

## 📚 DOCUMENTACIÓN ADICIONAL

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Stripe Webhook Security](https://stripe.com/docs/webhooks/signatures)
- [SQL Server Security](https://docs.microsoft.com/en-us/sql/relational-databases/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## ✅ ESTADO: COMPLETADO

Todas las capas de seguridad y auditoría han sido implementadas correctamente.

**Fecha de implementación:** 25 de abril de 2026

**Implementado por:** Kiro AI Assistant
