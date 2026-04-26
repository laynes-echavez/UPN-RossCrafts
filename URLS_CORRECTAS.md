# 🔗 URLs Correctas del Sistema - Ross Crafts

## ⚠️ IMPORTANTE: URLs Actualizadas

Las URLs de autenticación tienen el prefijo `/auth/`, no están en la raíz.

---

## 🏢 EMPLEADOS DEL SISTEMA

### Login de Empleados
```
✅ CORRECTO: http://127.0.0.1:8000/auth/login/
❌ INCORRECTO: http://127.0.0.1:8000/login/
```

### Logout de Empleados
```
✅ CORRECTO: http://127.0.0.1:8000/auth/logout/
❌ INCORRECTO: http://127.0.0.1:8000/logout/
```

### Dashboard Redirect
```
✅ CORRECTO: http://127.0.0.1:8000/auth/dashboard/
❌ INCORRECTO: http://127.0.0.1:8000/dashboard/
```

### Acceso Denegado
```
✅ CORRECTO: http://127.0.0.1:8000/auth/acceso-denegado/
```

---

## 🛒 CLIENTES DEL ECOMMERCE

### Login de Clientes
```
✅ CORRECTO: http://127.0.0.1:8000/cuenta/login/
```

### Registro de Clientes
```
✅ CORRECTO: http://127.0.0.1:8000/cuenta/registro/
```

### Logout de Clientes
```
✅ CORRECTO: http://127.0.0.1:8000/cuenta/logout/
```

### Perfil de Cliente
```
✅ CORRECTO: http://127.0.0.1:8000/cuenta/perfil/
```

---

## 📦 PANEL ADMINISTRATIVO

### Stock/Productos
```
http://127.0.0.1:8000/stock/productos/
http://127.0.0.1:8000/stock/productos/nuevo/
http://127.0.0.1:8000/stock/productos/<id>/editar/
http://127.0.0.1:8000/stock/productos/<id>/detalle/
http://127.0.0.1:8000/stock/importar/
```

### Clientes (Admin)
```
http://127.0.0.1:8000/clientes/
http://127.0.0.1:8000/clientes/nuevo/
http://127.0.0.1:8000/clientes/<id>/editar/
http://127.0.0.1:8000/clientes/<id>/perfil/
```

### Ventas (POS)
```
http://127.0.0.1:8000/dashboard/pos/
```

### Reportes
```
http://127.0.0.1:8000/reports/
```

### Auditoría
```
http://127.0.0.1:8000/dashboard/auditoria/
```

---

## 🏪 TIENDA ONLINE

### Página Principal
```
http://127.0.0.1:8000/
```

### Catálogo de Productos
```
http://127.0.0.1:8000/tienda/
```

### Detalle de Producto
```
http://127.0.0.1:8000/tienda/<slug>/
```

### Carrito
```
http://127.0.0.1:8000/carrito/
```

### Checkout
```
http://127.0.0.1:8000/checkout/
```

---

## 🔑 Credenciales de Prueba

### EMPLEADOS (usar en /auth/login/)
```
Gerente:
  Usuario: gerente
  Contraseña: gerente123

Administrador:
  Usuario: admin
  Contraseña: admin123

Empleado:
  Usuario: empleado1
  Contraseña: empleado123
```

### CLIENTES (usar en /cuenta/login/)
```
Cliente 1:
  Email: juan.cliente@gmail.com
  Contraseña: cliente123

Cliente 2:
  Email: maria.cliente@gmail.com
  Contraseña: cliente123
```

---

## 📝 Nombres de URLs en el Código

### Para usar en redirect() o reverse()

#### Empleados
```python
# Login
redirect('authentication:login')  # → /auth/login/

# Logout
redirect('authentication:logout')  # → /auth/logout/

# Dashboard
redirect('authentication:dashboard_redirect')  # → /auth/dashboard/

# Acceso denegado
redirect('authentication:access_denied')  # → /auth/acceso-denegado/
```

#### Clientes
```python
# Login
redirect('ecommerce:customer_login')  # → /cuenta/login/

# Registro
redirect('ecommerce:customer_register')  # → /cuenta/registro/

# Logout
redirect('ecommerce:customer_logout')  # → /cuenta/logout/

# Perfil
redirect('ecommerce:customer_profile')  # → /cuenta/perfil/

# Tienda
redirect('ecommerce:catalog')  # → /tienda/

# Home
redirect('ecommerce:home')  # → /
```

#### Admin
```python
# Productos
redirect('stock:product_list')  # → /stock/productos/
redirect('stock:product_create')  # → /stock/productos/nuevo/

# Clientes
redirect('customers:customer_list')  # → /clientes/

# POS
redirect('sales:pos')  # → /dashboard/pos/

# Reportes
redirect('reports:dashboard')  # → /reports/
```

---

## ⚡ Accesos Rápidos para Pruebas

### Empleados
1. Login: http://127.0.0.1:8000/auth/login/
2. Ver productos: http://127.0.0.1:8000/stock/productos/
3. POS: http://127.0.0.1:8000/dashboard/pos/
4. Clientes: http://127.0.0.1:8000/clientes/

### Clientes
1. Login: http://127.0.0.1:8000/cuenta/login/
2. Registro: http://127.0.0.1:8000/cuenta/registro/
3. Tienda: http://127.0.0.1:8000/tienda/
4. Carrito: http://127.0.0.1:8000/carrito/
5. Perfil: http://127.0.0.1:8000/cuenta/perfil/

---

## 🔧 Configuración en settings.py

```python
# URLs de autenticación
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/auth/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'
```

---

**Nota:** Todos los documentos de prueba han sido actualizados con las URLs correctas.

**Fecha de actualización:** 2026-04-26
