# Guía de Uso - Sistema de Autenticación Ross Crafts

## Índice
1. [Decoradores para Vistas Funcionales](#decoradores)
2. [Mixins para Vistas Basadas en Clase](#mixins)
3. [Middleware de Auditoría](#middleware)
4. [Configuración de Sesiones](#sesiones)
5. [Rate Limiting](#rate-limiting)
6. [Ejemplos Prácticos](#ejemplos)

---

## Decoradores

### @role_required

Decorador para controlar acceso por roles en vistas funcionales.

#### Uso Básico

```python
from apps.authentication.decorators import role_required

# Un solo rol
@role_required('gerente')
def mi_vista(request):
    return render(request, 'template.html')

# Múltiples roles
@role_required(['gerente', 'administrador'])
def mi_vista(request):
    return render(request, 'template.html')
```

#### Comportamiento

- ✅ Usuario autenticado con rol correcto → Acceso permitido
- ❌ Usuario no autenticado → Redirige a `/auth/login/`
- ❌ Usuario con rol incorrecto → Redirige a `/auth/acceso-denegado/`

---

## Mixins

### RoleRequiredMixin

Mixin para controlar acceso por roles en vistas basadas en clase.

#### Uso Básico

```python
from apps.authentication.mixins import RoleRequiredMixin
from django.views.generic import ListView

class MiVista(RoleRequiredMixin, ListView):
    allowed_roles = ['gerente', 'administrador']
    model = MiModelo
    template_name = 'template.html'
```

#### Crear Mixins Personalizados

```python
class GerenteRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['gerente']

class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['gerente', 'administrador']

# Uso
class MiVista(GerenteRequiredMixin, ListView):
    model = MiModelo
```

---

## Middleware

### AuditMiddleware

Registra automáticamente todas las peticiones de usuarios autenticados.

#### Información Registrada

- Usuario
- Método HTTP (GET, POST, etc.)
- URL accedida
- IP del cliente
- Código de estado HTTP
- Timestamp

#### Configuración

Ya está configurado en `settings/base.py`:

```python
MIDDLEWARE = [
    # ...
    'apps.authentication.middleware.AuditMiddleware',
]
```

#### Ver Logs

```python
from apps.audit.models import AuditLog

# Últimos 10 logs
logs = AuditLog.objects.all().order_by('-timestamp')[:10]

# Logs de un usuario
logs = AuditLog.objects.filter(user=request.user)

# Logs de login
logs = AuditLog.objects.filter(action='LOGIN')
```

---

## Sesiones

### Configuración Actual

```python
SESSION_COOKIE_AGE = 1800  # 30 minutos
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

### Personalizar Timeout

En `settings/base.py`:

```python
# 1 hora
SESSION_COOKIE_AGE = 3600

# 2 horas
SESSION_COOKIE_AGE = 7200

# 24 horas
SESSION_COOKIE_AGE = 86400
```

---

## Rate Limiting

### Configuración en Login

```python
@ratelimit(key='ip', rate='5/15m', method='POST', block=True)
def login_view(request):
    # ...
```

### Personalizar Rate Limiting

```python
from django_ratelimit.decorators import ratelimit

# 10 intentos por hora
@ratelimit(key='ip', rate='10/h', method='POST')
def mi_vista(request):
    pass

# 3 intentos por minuto
@ratelimit(key='ip', rate='3/m', method='POST')
def mi_vista(request):
    pass

# Por usuario en lugar de IP
@ratelimit(key='user', rate='5/15m', method='POST')
def mi_vista(request):
    pass
```

---

## Ejemplos Prácticos

### Ejemplo 1: Vista Solo para Gerentes

```python
from apps.authentication.decorators import role_required

@role_required('gerente')
def reportes_financieros(request):
    # Solo gerentes pueden ver esto
    return render(request, 'reportes/financieros.html')
```

### Ejemplo 2: Vista para Gerentes y Administradores

```python
@role_required(['gerente', 'administrador'])
def gestion_productos(request):
    # Gerentes y administradores pueden ver esto
    products = Product.objects.all()
    return render(request, 'stock/gestion.html', {
        'products': products
    })
```

### Ejemplo 3: Vista con Lógica Condicional por Rol

```python
@role_required(['gerente', 'administrador', 'empleado'])
def dashboard(request):
    context = {}
    
    if request.user.role == 'gerente':
        context['puede_ver_reportes'] = True
        context['puede_editar'] = True
    elif request.user.role == 'administrador':
        context['puede_ver_reportes'] = False
        context['puede_editar'] = True
    else:  # empleado
        context['puede_ver_reportes'] = False
        context['puede_editar'] = False
    
    return render(request, 'dashboard.html', context)
```

### Ejemplo 4: ListView con Control de Acceso

```python
from apps.authentication.mixins import RoleRequiredMixin
from django.views.generic import ListView

class ProductListView(RoleRequiredMixin, ListView):
    allowed_roles = ['gerente', 'administrador', 'empleado']
    model = Product
    template_name = 'stock/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Empleados solo ven productos activos
        if self.request.user.role == 'empleado':
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('-created_at')
```

### Ejemplo 5: CreateView con Control de Acceso

```python
from django.views.generic import CreateView
from apps.authentication.mixins import RoleRequiredMixin

class ProductCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['gerente', 'administrador']
    model = Product
    fields = ['name', 'sku', 'category', 'price', 'cost_price', 'stock_quantity']
    template_name = 'stock/product_form.html'
    success_url = '/stock/'
    
    def form_valid(self, form):
        # Registrar quién creó el producto
        product = form.save(commit=False)
        # Aquí podrías agregar un campo created_by si lo tienes
        return super().form_valid(form)
```

### Ejemplo 6: Verificar Rol en Template

```django
{% if user.role == 'gerente' %}
    <a href="{% url 'reports:dashboard' %}">Ver Reportes</a>
{% endif %}

{% if user.role in 'gerente,administrador' %}
    <a href="{% url 'stock:product_create' %}">Crear Producto</a>
{% endif %}
```

### Ejemplo 7: Registrar Acción Personalizada en Audit

```python
from apps.audit.models import AuditLog

def mi_vista(request):
    # Tu lógica aquí
    
    # Registrar acción personalizada
    AuditLog.objects.create(
        user=request.user,
        action='CUSTOM',
        url=request.path,
        ip_address=get_client_ip(request),
        status_code=200
    )
    
    return render(request, 'template.html')
```

---

## Flujo de Autenticación

```
1. Usuario accede a /auth/login/
2. Ingresa credenciales
3. Sistema verifica (máx 5 intentos)
4. Si es válido:
   - Crea sesión
   - Registra en AuditLog
   - Redirige a /auth/dashboard/
5. Dashboard redirige según rol:
   - gerente → /reports/
   - administrador → /sales/pos/
   - empleado → /sales/pos/
```

---

## Flujo de Control de Acceso

```
1. Usuario intenta acceder a una vista protegida
2. Decorador/Mixin verifica:
   - ¿Está autenticado? → No: redirige a login
   - ¿Tiene el rol correcto? → No: redirige a acceso-denegado
   - ¿Tiene el rol correcto? → Sí: permite acceso
3. Middleware registra la petición en AuditLog
```

---

## Mejores Prácticas

### ✅ Hacer

- Usar `@role_required` para vistas funcionales
- Usar `RoleRequiredMixin` para vistas basadas en clase
- Crear mixins personalizados para roles comunes
- Verificar roles en templates cuando sea necesario
- Revisar logs de auditoría regularmente

### ❌ Evitar

- No verificar autenticación manualmente (usa decoradores)
- No hardcodear roles en múltiples lugares
- No ignorar los logs de auditoría
- No usar roles en URLs (usar decoradores)

---

## Troubleshooting

### Problema: "Demasiados intentos"

**Solución:** Esperar 15 minutos o limpiar rate limit:

```python
from django.core.cache import cache
cache.clear()
```

### Problema: Usuario no puede acceder

**Verificar:**
1. ¿Está autenticado?
2. ¿Tiene el rol correcto?
3. ¿El decorador tiene el rol correcto?

```python
# En shell
python manage.py shell

from apps.authentication.models import User
user = User.objects.get(username='empleado')
print(user.role)  # Verificar rol
```

### Problema: Sesión expira muy rápido

**Solución:** Aumentar `SESSION_COOKIE_AGE` en settings:

```python
SESSION_COOKIE_AGE = 3600  # 1 hora
```

---

## Recursos Adicionales

- **Documentación completa:** `AUTENTICACION_COMPLETADA.md`
- **Ejemplos de código:** `apps/authentication/examples.py`
- **Script de prueba:** `test_authentication.py`
- **Crear usuarios:** `create_test_users.py`

---

## Soporte

Para más información o problemas, consulta:
- Logs de auditoría en `/admin/audit/auditlog/`
- Documentación de Django: https://docs.djangoproject.com/
- django-ratelimit: https://django-ratelimit.readthedocs.io/
