# 🧪 Guía de Pruebas - Sistema de Usuarios Ross Crafts

## ✅ Usuarios Creados Exitosamente

Se han creado **4 empleados** y **5 clientes** para realizar pruebas completas del sistema.

---

## 🔐 EMPLEADOS DEL SISTEMA

### URL de Acceso
```
http://127.0.0.1:8000/auth/login/
```

### 1. GERENTE (Acceso Total)
```
Usuario: gerente
Contraseña: gerente123
Nombre: Carlos Rodríguez
Email: gerente@rosscrafts.com
```

**Permisos:**
- ✅ Acceso total al sistema
- ✅ Ver auditoría del sistema
- ✅ Crear/editar/eliminar usuarios
- ✅ Crear/editar/eliminar productos
- ✅ Gestionar clientes
- ✅ Realizar ventas (POS)
- ✅ Ver todos los reportes
- ✅ Importar/exportar datos

### 2. ADMINISTRADOR (Gestión Operativa)
```
Usuario: admin
Contraseña: admin123
Nombre: María González
Email: admin@rosscrafts.com
```

**Permisos:**
- ✅ Crear/editar productos
- ✅ Gestionar clientes
- ✅ Realizar ventas (POS)
- ✅ Ver reportes
- ✅ Importar/exportar productos
- ❌ No puede ver auditoría
- ❌ No puede eliminar productos (solo desactivar)

### 3. EMPLEADO 1 (Operaciones Básicas)
```
Usuario: empleado1
Contraseña: empleado123
Nombre: Juan Pérez
Email: empleado1@rosscrafts.com
```

**Permisos:**
- ✅ Ver productos
- ✅ Ver clientes
- ✅ Realizar ventas (POS)
- ✅ Buscar productos y clientes
- ❌ No puede crear/editar productos
- ❌ No puede crear/editar clientes
- ❌ No puede ver reportes completos

### 4. EMPLEADO 2 (Operaciones Básicas)
```
Usuario: empleado2
Contraseña: empleado123
Nombre: Ana Torres
Email: empleado2@rosscrafts.com
```

**Permisos:** Iguales a Empleado 1

---

## 🛒 CLIENTES DEL ECOMMERCE

### URL de Acceso
```
http://127.0.0.1:8000/cuenta/login/
```

### Cliente 1
```
Email: juan.cliente@gmail.com
Contraseña: cliente123
Nombre: Juan Martínez
DNI: 12345678
Dirección: Av. Los Artesanos 123, Trujillo
```

### Cliente 2
```
Email: maria.cliente@gmail.com
Contraseña: cliente123
Nombre: María López
DNI: 87654321
Dirección: Jr. Las Flores 456, Trujillo
```

### Cliente 3
```
Email: pedro.cliente@gmail.com
Contraseña: cliente123
Nombre: Pedro Sánchez
DNI: 11223344
Dirección: Calle Los Pinos 789, Trujillo
```

### Cliente 4
```
Email: lucia.cliente@gmail.com
Contraseña: cliente123
Nombre: Lucía Ramírez
DNI: 55667788
Dirección: Av. La Marina 321, Trujillo
```

### Cliente 5
```
Email: carlos.cliente@gmail.com
Contraseña: cliente123
Nombre: Carlos Vega
DNI: 99887766
Dirección: Jr. Independencia 654, Trujillo
```

---

## 🧪 PLAN DE PRUEBAS

### A. Pruebas de Empleados

#### 1. Pruebas con GERENTE
- [ ] Login exitoso en `/login/`
- [ ] Acceso al dashboard
- [ ] Ver lista de productos en `/stock/productos/`
- [ ] Crear nuevo producto en `/stock/productos/nuevo/`
- [ ] Editar producto existente
- [ ] **Eliminar producto** (solo gerente puede)
- [ ] Ver lista de clientes en `/clientes/`
- [ ] Crear nuevo cliente
- [ ] Editar cliente existente
- [ ] Realizar venta en POS `/dashboard/pos/`
- [ ] Ver auditoría del sistema (si está implementada)
- [ ] Importar productos desde Excel
- [ ] Ver reportes completos
- [ ] Logout exitoso

#### 2. Pruebas con ADMINISTRADOR
- [ ] Login exitoso en `/login/`
- [ ] Acceso al dashboard
- [ ] Ver lista de productos
- [ ] Crear nuevo producto
- [ ] Editar producto existente
- [ ] **Intentar eliminar producto** (debe fallar o solo desactivar)
- [ ] Ver lista de clientes
- [ ] Gestionar clientes
- [ ] Realizar venta en POS
- [ ] Ver reportes
- [ ] **Intentar acceder a auditoría** (debe fallar)
- [ ] Logout exitoso

#### 3. Pruebas con EMPLEADO
- [ ] Login exitoso en `/login/`
- [ ] Acceso al dashboard
- [ ] Ver lista de productos (solo lectura)
- [ ] **Intentar crear producto** (debe fallar)
- [ ] Ver lista de clientes (solo lectura)
- [ ] **Intentar editar cliente** (debe fallar)
- [ ] Realizar venta en POS
- [ ] Buscar productos en POS
- [ ] Buscar clientes en POS
- [ ] **Intentar acceder a reportes** (debe fallar o acceso limitado)
- [ ] Logout exitoso

### B. Pruebas de Clientes

#### 1. Pruebas de Navegación Anónima
- [ ] Acceder a la tienda `/tienda/`
- [ ] Ver productos disponibles
- [ ] Ver detalle de producto
- [ ] Agregar producto al carrito (sesión)
- [ ] Ver carrito `/carrito/`
- [ ] **Intentar hacer checkout** (debe redirigir a login)

#### 2. Pruebas de Registro
- [ ] Acceder a `/cuenta/registro/`
- [ ] Completar formulario de registro
- [ ] Verificar creación de cuenta
- [ ] Login automático después del registro
- [ ] Verificar redirección a tienda

#### 3. Pruebas de Login Cliente
- [ ] Login exitoso en `/cuenta/login/`
- [ ] Verificar redirección a tienda
- [ ] Ver navbar con nombre de usuario
- [ ] Acceder a perfil `/cuenta/perfil/`
- [ ] Ver historial de pedidos
- [ ] Logout exitoso

#### 4. Pruebas de Compra
- [ ] Login como cliente
- [ ] Navegar tienda
- [ ] Agregar productos al carrito
- [ ] Ver carrito con productos
- [ ] Modificar cantidades en carrito
- [ ] Eliminar productos del carrito
- [ ] Proceder al checkout
- [ ] Completar compra
- [ ] Ver confirmación de pedido
- [ ] Verificar pedido en perfil

#### 5. Pruebas de Perfil
- [ ] Acceder a perfil de cliente
- [ ] Ver datos personales
- [ ] Editar información personal
- [ ] Cambiar contraseña
- [ ] Ver historial de compras
- [ ] Ver detalles de pedidos anteriores

### C. Pruebas de Seguridad

#### 1. Separación de Contextos
- [ ] Cliente NO puede acceder a `/dashboard/`
- [ ] Cliente NO puede acceder a `/stock/`
- [ ] Cliente NO puede acceder a `/clientes/`
- [ ] Empleado NO puede acceder a `/cuenta/perfil/` de clientes
- [ ] Empleado NO puede ver carrito de clientes

#### 2. Permisos por Rol
- [ ] Empleado NO puede crear productos
- [ ] Empleado NO puede editar clientes
- [ ] Administrador NO puede eliminar productos
- [ ] Administrador NO puede ver auditoría
- [ ] Solo Gerente puede eliminar productos
- [ ] Solo Gerente puede ver auditoría

#### 3. Autenticación
- [ ] Acceso a rutas protegidas sin login redirige a login
- [ ] Login con credenciales incorrectas muestra error
- [ ] Logout cierra sesión correctamente
- [ ] No se puede acceder con sesión expirada

---

## 📊 MATRIZ DE PRUEBAS RÁPIDA

| Acción | Gerente | Admin | Empleado | Cliente |
|--------|---------|-------|----------|---------|
| Ver productos (admin) | ✅ | ✅ | ✅ | ❌ |
| Crear producto | ✅ | ✅ | ❌ | ❌ |
| Editar producto | ✅ | ✅ | ❌ | ❌ |
| Eliminar producto | ✅ | ❌ | ❌ | ❌ |
| Ver clientes (admin) | ✅ | ✅ | ✅ | ❌ |
| Crear cliente (admin) | ✅ | ✅ | ❌ | ❌ |
| Editar cliente | ✅ | ✅ | ❌ | ❌ |
| Realizar venta POS | ✅ | ✅ | ✅ | ❌ |
| Ver reportes | ✅ | ✅ | ❌ | ❌ |
| Ver auditoría | ✅ | ❌ | ❌ | ❌ |
| Navegar tienda | ✅ | ✅ | ✅ | ✅ |
| Agregar al carrito | ❌ | ❌ | ❌ | ✅ |
| Hacer checkout | ❌ | ❌ | ❌ | ✅ |
| Ver perfil propio | ❌ | ❌ | ❌ | ✅ |

---

## 🔧 COMANDOS ÚTILES

### Verificar usuarios creados
```bash
python manage.py shell
```
```python
from django.contrib.auth import get_user_model
from apps.customers.models import Customer

User = get_user_model()

# Ver empleados
print("Empleados:", User.objects.count())
for user in User.objects.all():
    print(f"  - {user.username} ({user.role})")

# Ver clientes
print("\nClientes:", Customer.objects.count())
for customer in Customer.objects.all():
    print(f"  - {customer.email} ({customer.full_name})")
```

### Resetear contraseña de un usuario
```bash
python manage.py shell
```
```python
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.get(username='gerente')
user.set_password('nueva_contraseña')
user.save()
```

### Resetear contraseña de un cliente
```bash
python manage.py shell
```
```python
from apps.customers.models import Customer

cliente = Customer.objects.get(email='juan.cliente@gmail.com')
cliente.set_password('nueva_contraseña')
cliente.save()
```

---

## 📝 NOTAS IMPORTANTES

1. **Dos sistemas de autenticación separados:**
   - Empleados usan `username` en `/login/`
   - Clientes usan `email` en `/cuenta/login/`

2. **Navbar inteligente:**
   - Detecta automáticamente el tipo de usuario
   - Muestra menú apropiado según contexto

3. **Carrito de compras:**
   - Usuarios anónimos: Carrito por sesión
   - Clientes autenticados: Carrito persistente
   - Al hacer login: Migración automática de carrito

4. **Gestión de empleados:**
   - Se crean desde el panel admin en `/clientes/`
   - NO a través del registro público

5. **Contraseñas:**
   - Todas las contraseñas están hasheadas con PBKDF2
   - Las contraseñas de prueba son simples para facilitar testing
   - En producción usar contraseñas seguras

---

## ✅ CHECKLIST DE VERIFICACIÓN FINAL

### Sistema de Autenticación
- [x] Empleados creados correctamente
- [x] Clientes creados correctamente
- [x] Contraseñas hasheadas
- [ ] Login de empleados funciona
- [ ] Login de clientes funciona
- [ ] Logout funciona correctamente

### Permisos y Roles
- [ ] Gerente tiene acceso total
- [ ] Administrador tiene permisos limitados
- [ ] Empleado solo puede consultar y vender
- [ ] Cliente solo accede a tienda

### Seguridad
- [ ] Separación de contextos funciona
- [ ] Rutas protegidas requieren autenticación
- [ ] Permisos se validan correctamente
- [ ] No hay acceso cruzado entre tipos de usuario

---

**Fecha de creación:** 2026-04-26  
**Versión:** 1.0  
**Estado:** ✅ Usuarios creados - Listo para pruebas
