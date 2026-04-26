# 🧪 Guía de Pruebas - Separación de Contextos

## ⚡ Pruebas Rápidas (5 minutos)

### ✅ Test 1: Cliente ve solo tienda

**Pasos:**
1. Ir a: http://127.0.0.1:8000/cuenta/login/
2. Login: `juan.cliente@gmail.com` / `cliente123`
3. Observar la navbar

**Resultado Esperado:**
```
✅ Ve: [Logo] Inicio | Tienda | [Juan ▼] | Carrito (0)
❌ NO ve: Dashboard, Productos, POS, Clientes, Reportes, Auditoría
✅ Fondo color crema
✅ Footer completo con redes sociales
```

---

### ✅ Test 2: Empleado ve panel admin

**Pasos:**
1. Cerrar sesión de cliente
2. Ir a: http://127.0.0.1:8000/auth/login/
3. Login: `empleado1` / `empleado123`
4. Observar la navbar

**Resultado Esperado:**
```
✅ Ve: Dashboard | Productos ▼ | Clientes | POS | [Juan Pérez ▼]
❌ NO ve: Carrito, Reportes, Auditoría
✅ Fondo gris claro
✅ Footer simple
✅ Puede ver tienda en menú usuario
```

---

### ✅ Test 3: Administrador ve más opciones

**Pasos:**
1. Cerrar sesión
2. Login: `admin` / `admin123`
3. Observar la navbar

**Resultado Esperado:**
```
✅ Ve: Dashboard | Productos ▼ | Clientes | POS | Reportes | [María González ▼]
❌ NO ve: Auditoría (solo gerente)
✅ Puede crear productos
✅ Puede ver reportes
```

---

### ✅ Test 4: Gerente ve TODO

**Pasos:**
1. Cerrar sesión
2. Login: `gerente` / `gerente123`
3. Observar la navbar

**Resultado Esperado:**
```
✅ Ve: Dashboard | Productos ▼ | Clientes | POS | Reportes | Auditoría | [Carlos Rodríguez ▼]
✅ Todas las opciones visibles
✅ Puede eliminar productos
✅ Puede ver auditoría
```

---

### ✅ Test 5: Cliente NO puede acceder a admin

**Pasos:**
1. Login como cliente: `juan.cliente@gmail.com` / `cliente123`
2. Intentar acceder directamente a: http://127.0.0.1:8000/stock/productos/

**Resultado Esperado:**
```
✅ Redirige a: http://127.0.0.1:8000/tienda/
✅ Muestra mensaje: "Esta área es solo para empleados del sistema."
✅ Cliente nunca ve la interfaz administrativa
```

---

### ✅ Test 6: Visitante solo ve tienda

**Pasos:**
1. Cerrar todas las sesiones
2. Ir a: http://127.0.0.1:8000/

**Resultado Esperado:**
```
✅ Ve: [Logo] Inicio | Tienda | Iniciar Sesión | Registrarse | Carrito (0)
❌ NO ve: Opciones administrativas
✅ Puede navegar la tienda
✅ Puede agregar al carrito
```

---

## 📊 Matriz de Visibilidad

| Elemento de Navbar | Visitante | Cliente | Empleado | Admin | Gerente |
|-------------------|-----------|---------|----------|-------|---------|
| **TIENDA** |
| Inicio | ✅ | ✅ | ❌ | ❌ | ❌ |
| Tienda | ✅ | ✅ | ❌ | ❌ | ❌ |
| Carrito | ✅ | ✅ | ❌ | ❌ | ❌ |
| Login/Registro | ✅ | ❌ | ❌ | ❌ | ❌ |
| Mi Perfil | ❌ | ✅ | ❌ | ❌ | ❌ |
| Mis Pedidos | ❌ | ✅ | ❌ | ❌ | ❌ |
| **ADMIN** |
| Dashboard | ❌ | ❌ | ✅ | ✅ | ✅ |
| Productos | ❌ | ❌ | ✅ | ✅ | ✅ |
| Stock Bajo | ❌ | ❌ | ✅ | ✅ | ✅ |
| Clientes | ❌ | ❌ | ✅ | ✅ | ✅ |
| POS | ❌ | ❌ | ✅ | ✅ | ✅ |
| Reportes | ❌ | ❌ | ❌ | ✅ | ✅ |
| Auditoría | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ver Tienda | ❌ | ❌ | ✅ | ✅ | ✅ |

---

## 🎨 Diferencias Visuales

### Panel Administrativo
```
Fondo: Gris claro (#F9FAFB)
Navbar: Verde oscuro con menús desplegables
Footer: Simple, solo copyright
Estilo: Profesional, productivo
```

### Tienda Online
```
Fondo: Crema (#F8F3E1)
Navbar: Verde oscuro con carrito
Footer: Completo con contacto y redes
Estilo: Atractivo, comercial
```

---

## 🔍 Verificación de URLs

### URLs de Empleados
```
✅ Login: /auth/login/
✅ Dashboard: /auth/dashboard/
✅ Productos: /stock/productos/
✅ Clientes: /clientes/
✅ POS: /dashboard/pos/
✅ Reportes: /reports/
✅ Auditoría: /dashboard/auditoria/
```

### URLs de Clientes
```
✅ Login: /cuenta/login/
✅ Registro: /cuenta/registro/
✅ Tienda: /tienda/
✅ Carrito: /carrito/
✅ Perfil: /cuenta/perfil/
✅ Pedidos: /cuenta/mis-pedidos/
✅ Checkout: /checkout/
```

---

## ⚠️ Errores que NO deben aparecer

### ❌ Error 1: AttributeError 'role'
```
Este error ya NO debe aparecer
Cliente accede a vista admin → Redirige correctamente
```

### ❌ Error 2: Cliente ve opciones admin
```
Cliente NUNCA debe ver:
- Dashboard
- Productos (admin)
- POS
- Clientes (admin)
- Reportes
- Auditoría
```

### ❌ Error 3: Empleado ve carrito
```
Empleado NO debe ver:
- Carrito de compras en navbar
- Opciones de checkout
- Mi Perfil (de cliente)
```

---

## 📝 Checklist de Verificación

### Separación de Interfaces
- [ ] Cliente ve navbar de tienda
- [ ] Empleado ve navbar administrativa
- [ ] Visitante ve navbar pública
- [ ] Cada uno tiene su propio footer

### Permisos
- [ ] Cliente NO puede acceder a /stock/productos/
- [ ] Cliente NO puede acceder a /dashboard/pos/
- [ ] Empleado NO puede eliminar productos
- [ ] Solo gerente puede ver auditoría

### Navegación
- [ ] Cliente puede navegar tienda sin problemas
- [ ] Empleado puede acceder a todas sus vistas
- [ ] Redirecciones funcionan correctamente
- [ ] Mensajes de error son claros

### Visual
- [ ] Panel admin tiene fondo gris
- [ ] Tienda tiene fondo crema
- [ ] Navbars son diferentes
- [ ] Footers son apropiados

---

## 🎯 Resultado Final Esperado

Después de todas las pruebas:

✅ **Cliente:**
- Ve solo la tienda
- Puede comprar sin confusión
- No ve opciones administrativas
- Experiencia de ecommerce limpia

✅ **Empleado:**
- Ve solo panel administrativo
- Puede trabajar sin distracciones
- Acceso según su rol
- Puede ver tienda si necesita

✅ **Gerente:**
- Acceso total al sistema
- Todas las herramientas disponibles
- Control completo

✅ **Visitante:**
- Puede explorar la tienda
- Puede registrarse
- Interfaz atractiva

---

**Tiempo de prueba:** 5-10 minutos  
**Prioridad:** CRÍTICA  
**Estado:** Listo para probar
