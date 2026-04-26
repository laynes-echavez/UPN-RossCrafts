# 🧪 Guía de Pruebas - Fix Separación Cliente/Empleado

## ⚡ Pruebas Rápidas (2 minutos)

### ✅ Test 1: Cliente NO puede acceder a panel admin

**Pasos:**
1. Ir a: http://127.0.0.1:8000/cuenta/login/
2. Login: `juan.cliente@gmail.com` / `cliente123`
3. Intentar acceder a: http://127.0.0.1:8000/stock/productos/

**Resultado Esperado:**
- ✅ Redirige a la tienda
- ✅ Muestra mensaje: "Esta área es solo para empleados del sistema."
- ✅ NO muestra error AttributeError

---

### ✅ Test 2: Cliente puede hacer logout

**Pasos:**
1. Login como cliente: `juan.cliente@gmail.com` / `cliente123`
2. Navegar a la tienda
3. Hacer clic en "Cerrar Sesión" o ir a: http://127.0.0.1:8000/auth/logout/

**Resultado Esperado:**
- ✅ Logout exitoso
- ✅ Redirige a: http://127.0.0.1:8000/cuenta/login/
- ✅ Muestra mensaje: "Has cerrado sesión exitosamente."
- ✅ NO muestra error ValueError

---

### ✅ Test 3: Empleado puede hacer logout

**Pasos:**
1. Login como empleado: `empleado1` / `empleado123`
2. Hacer logout

**Resultado Esperado:**
- ✅ Logout exitoso
- ✅ Redirige a: http://127.0.0.1:8000/auth/login/
- ✅ Muestra mensaje: "Has cerrado sesión exitosamente."
- ✅ Se crea registro en AuditLog

---

### ✅ Test 4: Empleado sin permisos

**Pasos:**
1. Login como empleado: `empleado1` / `empleado123`
2. Intentar acceder a: http://127.0.0.1:8000/stock/productos/nuevo/

**Resultado Esperado:**
- ✅ Acceso denegado
- ✅ Muestra mensaje: "No tienes permisos para acceder a esta página."
- ✅ Redirige a página de acceso denegado

---

## 🔍 Verificación de Logs

### Verificar AuditLog (Solo Empleados)

```bash
python manage.py shell
```

```python
from apps.audit.models import AuditLog

# Ver últimos 10 registros
for log in AuditLog.objects.all().order_by('-created_at')[:10]:
    print(f"{log.user.username} - {log.action} - {log.created_at}")

# Verificar que NO hay registros de clientes
# (todos los registros deben tener user.username, no customer.email)
```

---

## 📊 Checklist Completo

### Clientes
- [ ] Cliente puede hacer login en `/cuenta/login/`
- [ ] Cliente puede navegar la tienda
- [ ] Cliente puede agregar productos al carrito
- [ ] Cliente puede hacer logout sin errores
- [ ] Cliente NO puede acceder a `/stock/productos/`
- [ ] Cliente NO puede acceder a `/dashboard/`
- [ ] Cliente NO puede acceder a `/clientes/`
- [ ] Cliente recibe mensaje apropiado al intentar acceder a admin

### Empleados
- [ ] Empleado puede hacer login en `/login/`
- [ ] Empleado puede acceder a vistas según su rol
- [ ] Empleado puede hacer logout sin errores
- [ ] Empleado con rol 'empleado' NO puede crear productos
- [ ] Empleado con rol 'administrador' puede crear productos
- [ ] Empleado con rol 'gerente' puede eliminar productos
- [ ] Logout de empleado crea registro en AuditLog

### Seguridad
- [ ] No hay errores AttributeError con clientes
- [ ] No hay errores ValueError en logout
- [ ] AuditLog solo registra acciones de empleados
- [ ] Mensajes de error son claros y apropiados
- [ ] Redirecciones funcionan correctamente

---

## 🐛 Errores que YA NO deben aparecer

### ❌ Error 1 (RESUELTO)
```
AttributeError at /stock/productos/
'Customer' object has no attribute 'role'
```

### ❌ Error 2 (RESUELTO)
```
ValueError at /auth/logout/
Cannot assign "<SimpleLazyObject: <Customer: Juan Martínez>>": 
"AuditLog.user" must be a "User" instance.
```

---

## 💡 Comandos Útiles

### Ver usuarios activos
```bash
python manage.py shell
```
```python
from django.contrib.auth import get_user_model
from apps.customers.models import Customer

User = get_user_model()

print("Empleados:")
for u in User.objects.all():
    print(f"  {u.username} - {u.role}")

print("\nClientes:")
for c in Customer.objects.all():
    print(f"  {c.email} - {c.full_name}")
```

### Limpiar sesiones
```bash
python manage.py clearsessions
```

---

## 🎯 Resultado Final

Si todas las pruebas pasan:
- ✅ Sistema de autenticación funciona correctamente
- ✅ Separación cliente/empleado es efectiva
- ✅ No hay errores de tipo de usuario
- ✅ AuditLog funciona solo para empleados
- ✅ Redirecciones son apropiadas
- ✅ Mensajes de error son claros

---

**Tiempo estimado:** 2-5 minutos  
**Prioridad:** CRÍTICA - Debe funcionar antes de continuar
