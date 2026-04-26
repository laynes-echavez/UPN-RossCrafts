# 🔐 Sistema de Roles y Permisos - Ross Crafts

## 📋 Tabla de Contenidos
1. [Tipos de Usuarios](#tipos-de-usuarios)
2. [Matriz de Permisos](#matriz-de-permisos)
3. [Credenciales de Prueba](#credenciales-de-prueba)
4. [Flujos de Autenticación](#flujos-de-autenticación)

---

## 👥 Tipos de Usuarios

### 1. **EMPLEADOS DEL SISTEMA** (Model: `User`)
Usuarios internos que gestionan el negocio a través del panel administrativo.

#### 🏆 **GERENTE**
- **Rol:** `gerente`
- **Permisos:** Acceso total al sistema
- **Puede:**
  - ✅ Gestionar todos los módulos
  - ✅ Ver auditoría del sistema
  - ✅ Crear/editar/eliminar usuarios
  - ✅ Crear/editar/eliminar productos
  - ✅ Gestionar clientes
  - ✅ Realizar ventas (POS)
  - ✅ Ver reportes completos
  - ✅ Importar/exportar datos
  - ✅ Desactivar productos y clientes

#### 👔 **ADMINISTRADOR**
- **Rol:** `administrador`
- **Permisos:** Gestión operativa
- **Puede:**
  - ✅ Crear/editar productos
  - ✅ Gestionar clientes
  - ✅ Realizar ventas (POS)
  - ✅ Ver reportes
  - ✅ Importar/exportar productos
  - ❌ No puede ver auditoría
  - ❌ No puede eliminar productos (solo desactivar)

#### 👤 **EMPLEADO**
- **Rol:** `empleado`
- **Permisos:** Operaciones básicas
- **Puede:**
  - ✅ Ver productos
  - ✅ Ver clientes
  - ✅ Realizar ventas (POS)
  - ✅ Buscar productos y clientes
  - ❌ No puede crear/editar productos
  - ❌ No puede crear/editar clientes
  - ❌ No puede ver reportes completos
  - ❌ No puede importar/exportar

### 2. **CLIENTES DEL ECOMMERCE** (Model: `Customer`)
Usuarios externos que compran a través de la tienda online.

#### 🛒 **CLIENTE**
- **Autenticación:** Email + Contraseña
- **Puede:**
  - ✅ Navegar la tienda
  - ✅ Agregar productos al carrito
  - ✅ Realizar compras online
  - ✅ Ver su perfil
  - ✅ Ver historial de pedidos
  - ✅ Actualizar sus datos personales
  - ✅ Cambiar contraseña
  - ❌ No tiene acceso al panel administrativo

---

## 📊 Matriz de Permisos

| Módulo / Acción | Gerente | Administrador | Empleado | Cliente |
|-----------------|---------|---------------|----------|---------|
| **PRODUCTOS** |
| Ver lista | ✅ | ✅ | ✅ | ✅ (tienda) |
| Ver detalle | ✅ | ✅ | ✅ | ✅ (tienda) |
| Crear | ✅ | ✅ | ❌ | ❌ |
| Editar | ✅ | ✅ | ❌ | ❌ |
| Eliminar | ✅ | ❌ | ❌ | ❌ |
| Importar Excel | ✅ | ✅ | ❌ | ❌ |
| **CLIENTES** |
| Ver lista | ✅ | ✅ | ✅ | ❌ |
| Ver perfil | ✅ | ✅ | ✅ | ✅ (propio) |
| Crear | ✅ | ✅ | ❌ | ✅ (registro) |
| Editar | ✅ | ✅ | ❌ | ✅ (propio) |
| Desactivar | ✅ | ✅ | ❌ | ❌ |
| Exportar Excel | ✅ | ✅ | ❌ | ❌ |
| **VENTAS (POS)** |
| Realizar venta | ✅ | ✅ | ✅ | ❌ |
| Ver historial | ✅ | ✅ | ✅ | ❌ |
| Imprimir comprobante | ✅ | ✅ | ✅ | ❌ |
| **PEDIDOS ONLINE** |
| Ver todos | ✅ | ✅ | ❌ | ❌ |
| Ver propios | ❌ | ❌ | ❌ | ✅ |
| Procesar | ✅ | ✅ | ❌ | ❌ |
| **REPORTES** |
| Ver reportes | ✅ | ✅ | ❌ | ❌ |
| Exportar | ✅ | ✅ | ❌ | ❌ |
| **AUDITORÍA** |
| Ver logs | ✅ | ❌ | ❌ | ❌ |
| **CARRITO** |
| Agregar productos | ❌ | ❌ | ❌ | ✅ |
| Realizar checkout | ❌ | ❌ | ❌ | ✅ |

---

## 🔑 Credenciales de Prueba

### 🏢 EMPLEADOS DEL SISTEMA
**URL de acceso:** http://127.0.0.1:8000/auth/login/

#### Gerente
```
Usuario: gerente
Contraseña: gerente123
Email: gerente@rosscrafts.com
Nombre: Carlos Rodríguez
```

#### Administrador
```
Usuario: admin
Contraseña: admin123
Email: admin@rosscrafts.com
Nombre: María González
```

#### Empleado 1
```
Usuario: empleado1
Contraseña: empleado123
Email: empleado1@rosscrafts.com
Nombre: Juan Pérez
```

#### Empleado 2
```
Usuario: empleado2
Contraseña: empleado123
Email: empleado2@rosscrafts.com
Nombre: Ana Torres
```

### 🛒 CLIENTES DEL ECOMMERCE
**URL de acceso:** http://127.0.0.1:8000/cuenta/login/

#### Cliente 1
```
Email: juan.cliente@gmail.com
Contraseña: cliente123
Nombre: Juan Martínez
DNI: 12345678
```

#### Cliente 2
```
Email: maria.cliente@gmail.com
Contraseña: cliente123
Nombre: María López
DNI: 87654321
```

#### Cliente 3
```
Email: pedro.cliente@gmail.com
Contraseña: cliente123
Nombre: Pedro Sánchez
DNI: 11223344
```

#### Cliente 4
```
Email: lucia.cliente@gmail.com
Contraseña: cliente123
Nombre: Lucía Ramírez
DNI: 55667788
```

#### Cliente 5
```
Email: carlos.cliente@gmail.com
Contraseña: cliente123
Nombre: Carlos Vega
DNI: 99887766
```

---

## 🔄 Flujos de Autenticación

### 1. Autenticación de Empleados

```
┌─────────────────────────────────────────┐
│  Usuario accede a /login/              │
├─────────────────────────────────────────┤
│  Ingresa: username + password          │
├─────────────────────────────────────────┤
│  Sistema valida contra User model      │
├─────────────────────────────────────────┤
│  ✅ Éxito → Redirige a Dashboard       │
│  ❌ Error → Muestra mensaje de error   │
└─────────────────────────────────────────┘
```

**Características:**
- Usa `username` para login
- Backend: `django.contrib.auth`
- Sesión: Django session framework
- Permisos: Basados en `role` y `is_staff`

### 2. Autenticación de Clientes

```
┌─────────────────────────────────────────┐
│  Cliente accede a /cuenta/login/       │
├─────────────────────────────────────────┤
│  Ingresa: email + password             │
├─────────────────────────────────────────┤
│  Sistema valida contra Customer model  │
├─────────────────────────────────────────┤
│  ✅ Éxito → Redirige a Tienda/Perfil   │
│  ❌ Error → Muestra mensaje de error   │
└─────────────────────────────────────────┘
```

**Características:**
- Usa `email` para login
- Backend: `CustomerAuthBackend` (custom)
- Sesión: Django session framework
- Permisos: Solo acceso a tienda y perfil

### 3. Registro de Clientes

```
┌─────────────────────────────────────────┐
│  Usuario accede a /cuenta/registro/    │
├─────────────────────────────────────────┤
│  Completa formulario de registro       │
├─────────────────────────────────────────┤
│  Sistema crea Customer                 │
├─────────────────────────────────────────┤
│  Envía email de bienvenida             │
├─────────────────────────────────────────┤
│  Login automático                       │
├─────────────────────────────────────────┤
│  Redirige a tienda                      │
└─────────────────────────────────────────┘
```

---

## 🛠️ Implementación Técnica

### Decoradores de Permisos

#### Para Empleados
```python
from apps.authentication.decorators import role_required

@role_required(['gerente', 'administrador'])
def vista_admin(request):
    # Solo gerentes y administradores
    pass
```

#### Para Clientes
```python
from apps.ecommerce.decorators import customer_login_required

@customer_login_required
def perfil_cliente(request):
    # Solo clientes autenticados
    pass
```

### Mixins para Vistas Basadas en Clases

```python
from apps.authentication.mixins import RoleRequiredMixin

class ProductListView(RoleRequiredMixin, ListView):
    allowed_roles = ['gerente', 'administrador', 'empleado']
    model = Product
```

---

## 📝 Notas Importantes

1. **Separación de Contextos:**
   - Empleados → Panel Admin (`/dashboard/`, `/stock/`, `/clientes/`, etc.)
   - Clientes → Tienda (`/`, `/tienda/`, `/carrito/`, `/cuenta/`)

2. **Seguridad:**
   - Contraseñas hasheadas con PBKDF2
   - CSRF protection habilitado
   - Session timeout configurable

3. **Navegación:**
   - Navbar detecta tipo de usuario automáticamente
   - Muestra menú apropiado según contexto

4. **Carrito de Compras:**
   - Usuarios anónimos: Carrito por sesión
   - Clientes autenticados: Carrito persistente
   - Al login: Migración automática de carrito

---

## 🚀 Cómo Crear los Usuarios de Prueba

```bash
# Opción 1: Usando el script
python manage.py shell < create_test_users.py

# Opción 2: Manualmente en shell
python manage.py shell
>>> exec(open('create_test_users.py').read())
```

---

## ✅ Checklist de Pruebas

### Empleados
- [ ] Login como gerente
- [ ] Acceso a auditoría (solo gerente)
- [ ] Crear/editar producto
- [ ] Eliminar producto (solo gerente)
- [ ] Realizar venta en POS
- [ ] Ver reportes

### Clientes
- [ ] Registro de nuevo cliente
- [ ] Login como cliente
- [ ] Navegar tienda
- [ ] Agregar productos al carrito
- [ ] Ver perfil
- [ ] Ver historial de pedidos
- [ ] Cambiar contraseña

### Seguridad
- [ ] Cliente no puede acceder a `/dashboard/`
- [ ] Empleado no puede acceder a `/cuenta/perfil/`
- [ ] Empleado no puede eliminar productos
- [ ] Solo gerente puede ver auditoría

---

**Última actualización:** 2026-04-26
**Versión:** 1.0
