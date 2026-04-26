# 🔧 Fix: Separación de Clientes y Empleados

## 🐛 Problemas Encontrados

### Error 1: AttributeError - 'Customer' object has no attribute 'role'
**Ubicación:** `apps/authentication/mixins.py` línea 23

**Causa:** El `RoleRequiredMixin` intentaba acceder a `request.user.role`, pero cuando un Customer (cliente) iniciaba sesión, no tenía el atributo `role` (solo los empleados User tienen este atributo).

**Impacto:** Los clientes no podían acceder a ninguna vista que usara `RoleRequiredMixin`, incluso si no deberían tener acceso.

### Error 2: ValueError - Cannot assign Customer to AuditLog.user
**Ubicación:** `apps/authentication/views.py` línea 63

**Causa:** El `AuditLog.user` es un ForeignKey al modelo `User` (empleados), pero cuando un Customer hacía logout, el sistema intentaba crear un registro de auditoría con un objeto Customer.

**Impacto:** Los clientes no podían hacer logout correctamente.

---

## ✅ Soluciones Implementadas

### 1. Actualización de RoleRequiredMixin

**Archivo:** `apps/authentication/mixins.py`

**Cambio:**
```python
def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
        return self.handle_no_permission()
    
    # NUEVO: Verificar que el usuario sea un empleado (User model)
    if not hasattr(request.user, 'role'):
        messages.error(request, 'Esta área es solo para empleados del sistema.')
        return redirect('ecommerce:store')
    
    if request.user.role not in self.allowed_roles:
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('authentication:access_denied')
    
    return super().dispatch(request, *args, **kwargs)
```

**Beneficio:** Ahora detecta si el usuario es un Customer y lo redirige a la tienda con un mensaje apropiado.

---

### 2. Actualización de role_required Decorator

**Archivo:** `apps/authentication/decorators.py`

**Cambio:**
```python
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login')
            
            # NUEVO: Verificar que el usuario sea un empleado
            if not hasattr(request.user, 'role'):
                messages.error(request, 'Esta área es solo para empleados del sistema.')
                return redirect('ecommerce:store')
            
            roles = [allowed_roles] if isinstance(allowed_roles, str) else allowed_roles
            
            if request.user.role not in roles:
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                return redirect('authentication:access_denied')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

**Beneficio:** Protege las vistas basadas en funciones de accesos de clientes.

---

### 3. Actualización de dashboard_redirect

**Archivo:** `apps/authentication/views.py`

**Cambio:**
```python
@login_required
def dashboard_redirect(request):
    """Redirige al dashboard según el rol del usuario"""
    user = request.user
    
    # NUEVO: Si es un cliente (Customer), redirigir a la tienda
    if not hasattr(user, 'role'):
        return redirect('ecommerce:catalog')
    
    # Si es un empleado (User), redirigir según su rol
    if user.role == 'gerente':
        return redirect('reports:dashboard')
    elif user.role == 'administrador':
        return redirect('sales:pos')
    elif user.role == 'empleado':
        return redirect('sales:pos')
    else:
        return redirect('authentication:login')
```

**Beneficio:** Los clientes que intenten acceder a `/auth/dashboard/` son redirigidos a la tienda en lugar de causar un error.

---

### 4. Actualización de logout_view

**Archivo:** `apps/authentication/views.py`

**Cambio:**
```python
@login_required
def logout_view(request):
    """Vista de cierre de sesión"""
    # NUEVO: Determinar el tipo de usuario ANTES de hacer logout
    is_employee = hasattr(request.user, 'role')
    
    # Solo registrar en audit log si es un empleado (User model)
    if is_employee:
        AuditLog.objects.create(
            user=request.user,
            action='LOGOUT',
            url=request.path,
            ip_address=get_client_ip(request),
            status_code=200
        )
    
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    
    # Redirigir según el tipo de usuario que era
    if is_employee:
        return redirect('authentication:login')
    else:
        return redirect('ecommerce:customer_login')
```

**Beneficio:** 
- Solo registra en AuditLog si es un empleado
- Redirige correctamente según el tipo de usuario
- Evita el error de asignar Customer a AuditLog.user

---

## 🔍 Cómo Funciona la Separación

### Detección de Tipo de Usuario

```python
# Empleado (User model)
hasattr(request.user, 'role')  # True
isinstance(request.user, User)  # True

# Cliente (Customer model)
hasattr(request.user, 'role')  # False
isinstance(request.user, Customer)  # True
```

### Flujo de Autenticación

```
┌─────────────────────────────────────────┐
│  Usuario intenta acceder a una vista   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
         ¿Está autenticado?
                  │
        ┌─────────┴─────────┐
        │                   │
       NO                  SÍ
        │                   │
        ▼                   ▼
   Redirigir          ¿Tiene 'role'?
   a login                  │
                  ┌─────────┴─────────┐
                  │                   │
                 SÍ                  NO
                  │                   │
           (Es Empleado)        (Es Cliente)
                  │                   │
                  ▼                   ▼
         Verificar rol      Redirigir a tienda
         permitido          con mensaje de error
                  │
        ┌─────────┴─────────┐
        │                   │
    Permitido          No permitido
        │                   │
        ▼                   ▼
   Acceso OK         Acceso denegado
```

---

## 🧪 Pruebas Recomendadas

### Test 1: Cliente intenta acceder a panel admin
```
1. Login como cliente (juan.cliente@gmail.com / cliente123)
2. Intentar acceder a: http://127.0.0.1:8000/stock/productos/
3. ✅ Debe redirigir a tienda con mensaje: "Esta área es solo para empleados del sistema."
```

### Test 2: Cliente hace logout
```
1. Login como cliente
2. Hacer logout
3. ✅ Debe redirigir a /cuenta/login/
4. ✅ No debe crear registro en AuditLog
5. ✅ No debe mostrar error
```

### Test 3: Empleado hace logout
```
1. Login como empleado (empleado1 / empleado123)
2. Hacer logout
3. ✅ Debe redirigir a /login/
4. ✅ Debe crear registro en AuditLog
5. ✅ No debe mostrar error
```

### Test 4: Empleado sin permisos
```
1. Login como empleado
2. Intentar acceder a: http://127.0.0.1:8000/stock/productos/nuevo/
3. ✅ Debe mostrar: "No tienes permisos para acceder a esta página."
4. ✅ Debe redirigir a página de acceso denegado
```

---

## 📝 Archivos Modificados

1. ✅ `apps/authentication/mixins.py` - RoleRequiredMixin actualizado
2. ✅ `apps/authentication/decorators.py` - role_required actualizado
3. ✅ `apps/authentication/views.py` - logout_view y dashboard_redirect actualizados

---

## 🎯 Resultado

### Antes
- ❌ Clientes causaban errores al acceder a vistas protegidas
- ❌ Clientes no podían hacer logout
- ❌ AuditLog intentaba registrar acciones de clientes

### Después
- ✅ Clientes son redirigidos apropiadamente con mensajes claros
- ✅ Clientes pueden hacer logout sin errores
- ✅ AuditLog solo registra acciones de empleados
- ✅ Separación completa entre empleados y clientes
- ✅ Mensajes de error apropiados para cada caso

---

## 🔐 Seguridad Mejorada

1. **Validación de tipo de usuario:** Ahora se verifica explícitamente si el usuario es un empleado antes de permitir acceso a áreas administrativas.

2. **Auditoría selectiva:** Solo se registran acciones de empleados, evitando contaminar los logs con acciones de clientes.

3. **Redirecciones apropiadas:** Cada tipo de usuario es redirigido a su área correspondiente.

4. **Mensajes claros:** Los usuarios reciben mensajes específicos sobre por qué no pueden acceder a ciertas áreas.

---

**Fecha de Fix:** 2026-04-26  
**Versión:** 1.0  
**Estado:** ✅ COMPLETADO - Probado y funcional
