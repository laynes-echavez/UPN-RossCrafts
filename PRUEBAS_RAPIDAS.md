# ⚡ Pruebas Rápidas - Ross Crafts

## 🎯 Guía de Pruebas Express (5 minutos)

### 1️⃣ GERENTE (Acceso Total)
```
URL: http://127.0.0.1:8000/auth/login/
Usuario: gerente
Contraseña: gerente123
```

**Probar:**
- ✅ Ir a Productos → Crear nuevo producto
- ✅ Ir a Productos → Eliminar un producto
- ✅ Ir a POS → Realizar una venta
- ✅ Ir a Reportes → Ver reporte de ventas
- ✅ Ir a Auditoría (si existe)

---

### 2️⃣ ADMINISTRADOR (Gestión Operativa)
```
URL: http://127.0.0.1:8000/auth/login/
Usuario: admin
Contraseña: admin123
```

**Probar:**
- ✅ Ir a Productos → Crear nuevo producto (debe funcionar)
- ❌ Ir a Productos → Intentar eliminar (debe fallar)
- ✅ Ir a Clientes → Gestionar clientes
- ✅ Ir a POS → Realizar una venta
- ✅ Ir a Reportes → Ver reportes
- ❌ Ir a Auditoría (debe fallar)

---

### 3️⃣ EMPLEADO (Solo Ventas)
```
URL: http://127.0.0.1:8000/auth/login/
Usuario: empleado1
Contraseña: empleado123
```

**Probar:**
- ✅ Ir a Productos → Ver lista (solo lectura)
- ❌ Ir a Productos → Intentar crear (debe fallar)
- ✅ Ir a Clientes → Ver lista (solo lectura)
- ❌ Ir a Clientes → Intentar editar (debe fallar)
- ✅ Ir a POS → Realizar una venta
- ❌ Ir a Reportes (debe fallar)

---

### 4️⃣ CLIENTE (Tienda Online)
```
URL: http://127.0.0.1:8000/cuenta/login/
Email: juan.cliente@gmail.com
Contraseña: cliente123
```

**Probar:**
- ✅ Navegar la tienda
- ✅ Agregar productos al carrito
- ✅ Ver carrito
- ✅ Ver perfil
- ❌ Intentar acceder a /dashboard/ (debe fallar)
- ❌ Intentar acceder a /stock/ (debe fallar)

---

## 🔥 Pruebas de Seguridad (Críticas)

### Test 1: Separación de Contextos
```
1. Login como cliente (juan.cliente@gmail.com)
2. Intentar acceder a: http://127.0.0.1:8000/dashboard/
3. ❌ Debe redirigir o mostrar error
```

### Test 2: Permisos de Eliminación
```
1. Login como admin
2. Ir a un producto
3. Intentar eliminar
4. ❌ Debe fallar (solo gerente puede)
```

### Test 3: Permisos de Creación
```
1. Login como empleado1
2. Intentar acceder a: http://127.0.0.1:8000/stock/productos/nuevo/
3. ❌ Debe mostrar error de permisos
```

### Test 4: Auditoría Restringida
```
1. Login como admin
2. Intentar acceder a auditoría
3. ❌ Debe fallar (solo gerente)
```

---

## 📋 Checklist Rápido

### Empleados
- [ ] Gerente puede hacer TODO
- [ ] Admin NO puede eliminar productos
- [ ] Admin NO puede ver auditoría
- [ ] Empleado NO puede crear/editar productos
- [ ] Empleado NO puede ver reportes
- [ ] Todos pueden usar POS

### Clientes
- [ ] Cliente puede navegar tienda
- [ ] Cliente puede agregar al carrito
- [ ] Cliente puede ver su perfil
- [ ] Cliente NO puede acceder a /dashboard/
- [ ] Cliente NO puede acceder a /stock/

### Autenticación
- [ ] Login empleados funciona (/login/)
- [ ] Login clientes funciona (/cuenta/login/)
- [ ] Logout funciona correctamente
- [ ] Registro de clientes funciona

---

## 🚀 URLs de Prueba Directa

### Panel Administrativo (Empleados)
```
http://127.0.0.1:8000/auth/login/
http://127.0.0.1:8000/dashboard/
http://127.0.0.1:8000/stock/productos/
http://127.0.0.1:8000/stock/productos/nuevo/
http://127.0.0.1:8000/clientes/
http://127.0.0.1:8000/dashboard/pos/
http://127.0.0.1:8000/reportes/
```

### Tienda Online (Clientes)
```
http://127.0.0.1:8000/cuenta/login/
http://127.0.0.1:8000/cuenta/registro/
http://127.0.0.1:8000/tienda/
http://127.0.0.1:8000/carrito/
http://127.0.0.1:8000/cuenta/perfil/
```

---

## 💡 Tips de Prueba

1. **Usa ventanas de incógnito** para probar múltiples usuarios simultáneamente
2. **Verifica los mensajes de error** - deben ser claros y apropiados
3. **Prueba las redirecciones** - deben llevar a páginas lógicas
4. **Revisa la navbar** - debe mostrar opciones según el rol
5. **Intenta accesos directos por URL** - la seguridad debe funcionar

---

## 🎯 Resultado Esperado

| Usuario | Login | Dashboard | Crear Producto | Eliminar | POS | Reportes | Tienda | Carrito |
|---------|-------|-----------|----------------|----------|-----|----------|--------|---------|
| Gerente | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Admin | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| Empleado | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| Cliente | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

---

**Tiempo estimado:** 5-10 minutos  
**Prioridad:** Alta - Verificar antes de producción
