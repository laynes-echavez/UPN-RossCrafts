# 🎯 Lógica Simple y Clara de Roles

## 📊 Regla Principal

**TODOS los empleados ven la MISMA interfaz administrativa.**

La diferencia NO está en el diseño, sino en **qué pueden hacer**.

---

## 🖥️ 2 INTERFACES ÚNICAS

### 1. Panel Administrativo (`admin/base_admin.html`)
**Quién lo usa:** Empleado, Administrador, Gerente

**Todos ven:**
- Dashboard
- Productos
- Stock Bajo (si hay)
- Clientes
- POS
- Badge con su rol (Empleado/Administrador/Gerente)

**Diferencias por rol:**
- **Gerente:** Ve TODO + Reportes + Auditoría
- **Administrador:** Ve TODO + Reportes (sin Auditoría)
- **Empleado:** Ve TODO (sin Reportes ni Auditoría)

### 2. Tienda Online (`store/base_store.html`)
**Quién lo usa:** Clientes y Visitantes

**Todos ven:**
- Inicio
- Tienda
- Carrito
- Login/Registro (si no están autenticados)
- Perfil (si están autenticados)

---

## 🔑 Diferencias por Rol (SOLO PERMISOS)

### 👔 EMPLEADO
**Navbar:**
```
Dashboard | Productos | Stock Bajo | Clientes | POS | [Juan Pérez - Empleado ▼]
```

**Puede:**
- ✅ Ver productos
- ✅ Ver clientes
- ✅ Realizar ventas en POS
- ✅ Buscar productos y clientes

**NO puede:**
- ❌ Crear/editar productos (botones deshabilitados)
- ❌ Crear/editar clientes (botones deshabilitados)
- ❌ Ver reportes (no aparece en navbar)
- ❌ Ver auditoría (no aparece en navbar)
- ❌ Eliminar productos

### 👔 ADMINISTRADOR
**Navbar:**
```
Dashboard | Productos | Stock Bajo | Clientes | POS | Reportes | [María González - Administrador ▼]
```

**Puede:**
- ✅ Todo lo del Empleado +
- ✅ Crear/editar productos
- ✅ Crear/editar clientes
- ✅ Ver reportes
- ✅ Importar productos desde Excel
- ✅ Exportar datos

**NO puede:**
- ❌ Eliminar productos (solo desactivar)
- ❌ Ver auditoría (no aparece en navbar)

### 👔 GERENTE
**Navbar:**
```
Dashboard | Productos | Stock Bajo | Clientes | POS | Reportes | Auditoría | [Carlos Rodríguez - Gerente ▼]
```

**Puede:**
- ✅ TODO lo del Administrador +
- ✅ Eliminar productos
- ✅ Ver auditoría del sistema
- ✅ Acceso completo sin restricciones

---

## 🎨 Interfaz Consistente

### Todos los empleados ven:

**Misma navbar:**
- Mismo color verde oscuro
- Mismos iconos
- Mismo diseño
- Mismo fondo gris claro

**Mismas páginas:**
- Mismo diseño de lista de productos
- Mismo diseño de formularios
- Mismo diseño de POS
- Mismo diseño de clientes

**Diferencia visual ÚNICA:**
- Badge con su rol en la navbar: `[Empleado]` `[Administrador]` `[Gerente]`
- Opciones de menú que aparecen/desaparecen según rol

---

## 🔒 Control de Permisos

### En las Vistas (Backend)

```python
# Todos pueden ver
@role_required(['gerente', 'administrador', 'empleado'])
def product_list(request):
    pass

# Solo Gerente y Admin pueden crear
@role_required(['gerente', 'administrador'])
def product_create(request):
    pass

# Solo Gerente puede eliminar
@role_required(['gerente'])
def product_delete(request):
    pass
```

### En los Templates (Frontend)

```html
<!-- Todos ven el botón de ver -->
<a href="{% url 'stock:product_list' %}">Ver Productos</a>

<!-- Solo Gerente y Admin ven el botón de crear -->
{% if user.role == 'gerente' or user.role == 'administrador' %}
<a href="{% url 'stock:product_create' %}">Nuevo Producto</a>
{% endif %}

<!-- Solo Gerente ve el botón de eliminar -->
{% if user.role == 'gerente' %}
<button>Eliminar</button>
{% endif %}
```

---

## 📋 Matriz de Permisos Simple

| Acción | Empleado | Admin | Gerente |
|--------|----------|-------|---------|
| **PRODUCTOS** |
| Ver lista | ✅ | ✅ | ✅ |
| Ver detalle | ✅ | ✅ | ✅ |
| Crear | ❌ | ✅ | ✅ |
| Editar | ❌ | ✅ | ✅ |
| Eliminar | ❌ | ❌ | ✅ |
| Importar | ❌ | ✅ | ✅ |
| **CLIENTES** |
| Ver lista | ✅ | ✅ | ✅ |
| Ver perfil | ✅ | ✅ | ✅ |
| Crear | ❌ | ✅ | ✅ |
| Editar | ❌ | ✅ | ✅ |
| Desactivar | ❌ | ✅ | ✅ |
| Exportar | ❌ | ✅ | ✅ |
| **VENTAS** |
| POS | ✅ | ✅ | ✅ |
| Ver historial | ✅ | ✅ | ✅ |
| **REPORTES** |
| Ver reportes | ❌ | ✅ | ✅ |
| Exportar | ❌ | ✅ | ✅ |
| **AUDITORÍA** |
| Ver logs | ❌ | ❌ | ✅ |

---

## 🎯 Ejemplo Visual

### Empleado ve:
```
┌─────────────────────────────────────────────────────────┐
│ [Logo] Dashboard | Productos | Clientes | POS | [Juan - Empleado ▼] │
└─────────────────────────────────────────────────────────┘

En página de productos:
- ✅ Puede ver lista
- ❌ NO ve botón "Nuevo Producto"
- ❌ NO ve botón "Importar"
- ❌ NO ve botón "Eliminar"
```

### Administrador ve:
```
┌──────────────────────────────────────────────────────────────────┐
│ [Logo] Dashboard | Productos | Clientes | POS | Reportes | [María - Administrador ▼] │
└──────────────────────────────────────────────────────────────────┘

En página de productos:
- ✅ Puede ver lista
- ✅ VE botón "Nuevo Producto"
- ✅ VE botón "Importar"
- ❌ NO ve botón "Eliminar" (solo "Desactivar")
```

### Gerente ve:
```
┌────────────────────────────────────────────────────────────────────────────┐
│ [Logo] Dashboard | Productos | Clientes | POS | Reportes | Auditoría | [Carlos - Gerente ▼] │
└────────────────────────────────────────────────────────────────────────────┘

En página de productos:
- ✅ Puede ver lista
- ✅ VE botón "Nuevo Producto"
- ✅ VE botón "Importar"
- ✅ VE botón "Eliminar"
```

---

## 🔄 Flujo de Trabajo

### Empleado (Juan)
```
1. Login → /auth/login/
2. Ve navbar con: Dashboard, Productos, Clientes, POS
3. Va a Productos → Solo puede ver y buscar
4. Va a POS → Puede realizar ventas
5. Intenta crear producto → Botón no existe
6. Intenta ir a /stock/productos/nuevo/ → Error 403
```

### Administrador (María)
```
1. Login → /auth/login/
2. Ve navbar con: Dashboard, Productos, Clientes, POS, Reportes
3. Va a Productos → Puede ver, crear, editar
4. Crea nuevo producto → ✅ Funciona
5. Ve reportes → ✅ Funciona
6. Intenta eliminar producto → Botón no existe
7. Intenta ir a auditoría → No aparece en menú
```

### Gerente (Carlos)
```
1. Login → /auth/login/
2. Ve navbar con: Dashboard, Productos, Clientes, POS, Reportes, Auditoría
3. Puede hacer TODO
4. Ve auditoría → ✅ Funciona
5. Elimina producto → ✅ Funciona
6. Acceso completo sin restricciones
```

---

## ✅ Resumen

### Lógica Simple:
1. **Una sola interfaz administrativa** para todos los empleados
2. **Mismo diseño** para todos
3. **Diferentes permisos** según rol
4. **Opciones aparecen/desaparecen** según rol
5. **Badge visible** muestra el rol actual

### NO hay:
- ❌ Diferentes diseños por rol
- ❌ Diferentes colores por rol
- ❌ Diferentes layouts por rol
- ❌ Confusión sobre qué interfaz usar

### SÍ hay:
- ✅ Una interfaz consistente
- ✅ Permisos claros
- ✅ Rol visible en todo momento
- ✅ Botones/opciones según permisos

---

**Fecha:** 2026-04-26  
**Versión:** 3.0  
**Estado:** ✅ LÓGICA CLARA Y SIMPLE
