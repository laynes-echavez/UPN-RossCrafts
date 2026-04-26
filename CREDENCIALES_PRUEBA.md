# 🔑 Credenciales de Prueba - Ross Crafts

## 🏢 EMPLEADOS DEL SISTEMA
**URL:** http://127.0.0.1:8000/auth/login/

| Rol | Usuario | Contraseña | Nombre |
|-----|---------|------------|--------|
| 🏆 Gerente | `gerente` | `gerente123` | Carlos Rodríguez |
| 👔 Administrador | `admin` | `admin123` | María González |
| 👤 Empleado | `empleado1` | `empleado123` | Juan Pérez |
| 👤 Empleado | `empleado2` | `empleado123` | Ana Torres |

---

## 🛒 CLIENTES DEL ECOMMERCE
**URL:** http://127.0.0.1:8000/cuenta/login/

| Email | Contraseña | Nombre | DNI |
|-------|------------|--------|-----|
| `juan.cliente@gmail.com` | `cliente123` | Juan Martínez | 12345678 |
| `maria.cliente@gmail.com` | `cliente123` | María López | 87654321 |
| `pedro.cliente@gmail.com` | `cliente123` | Pedro Sánchez | 11223344 |
| `lucia.cliente@gmail.com` | `cliente123` | Lucía Ramírez | 55667788 |
| `carlos.cliente@gmail.com` | `cliente123` | Carlos Vega | 99887766 |

---

## 🎯 ACCESOS RÁPIDOS

### Panel Administrativo (Empleados)
- 🏠 Dashboard: http://127.0.0.1:8000/dashboard/
- 📦 Productos: http://127.0.0.1:8000/stock/productos/
- 👥 Clientes: http://127.0.0.1:8000/clientes/
- 💰 POS (Ventas): http://127.0.0.1:8000/dashboard/pos/
- 📊 Reportes: http://127.0.0.1:8000/reportes/

### Tienda Online (Clientes)
- 🏪 Tienda: http://127.0.0.1:8000/tienda/
- 🛒 Carrito: http://127.0.0.1:8000/carrito/
- 👤 Perfil: http://127.0.0.1:8000/cuenta/perfil/
- 📝 Registro: http://127.0.0.1:8000/cuenta/registro/

---

## 📋 PERMISOS RESUMIDOS

### 🏆 GERENTE
✅ TODO (acceso completo)

### 👔 ADMINISTRADOR
✅ Gestionar productos, clientes, ventas, reportes  
❌ Eliminar productos, ver auditoría

### 👤 EMPLEADO
✅ Ver productos/clientes, realizar ventas  
❌ Crear/editar productos/clientes, ver reportes

### 🛒 CLIENTE
✅ Navegar tienda, comprar, ver perfil  
❌ Acceso al panel administrativo

---

**Nota:** Todas las contraseñas son de prueba. En producción usar contraseñas seguras.
