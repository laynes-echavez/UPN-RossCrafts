# 🔄 GUÍA DE MIGRACIÓN AL NUEVO SISTEMA DE DISEÑO

## 📋 RESUMEN

Esta guía te ayudará a migrar los templates existentes al nuevo sistema de diseño unificado.

---

## 🎯 PASOS GENERALES

### 1. Actualizar el `<head>` del Template

**ANTES:**
```html
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```

**DESPUÉS:**
```html
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Sistema de Diseño -->
<link rel="stylesheet" href="{% static 'css/design-system.css' %}">
```

### 2. Reemplazar Clases de Botones

| ANTES | DESPUÉS |
|-------|---------|
| `btn-primary` (Bootstrap) | `btn btn-primary` |
| `btn-secondary` (Bootstrap) | `btn btn-secondary` |
| `btn-success` (Bootstrap) | `btn btn-success` |
| `btn-danger` (Bootstrap) | `btn btn-error` |
| `btn-warning` (Bootstrap) | `btn btn-warning` |
| `btn-sm` (Bootstrap) | `btn btn-sm` |
| `btn-lg` (Bootstrap) | `btn btn-lg` |

### 3. Reemplazar Clases de Formularios

| ANTES | DESPUÉS |
|-------|---------|
| `form-control` (Bootstrap) | `form-input` |
| `form-select` (Bootstrap) | `form-select` |
| `form-label` (Bootstrap) | `form-label` |
| `form-text` (Bootstrap) | `form-help` |
| `invalid-feedback` (Bootstrap) | `form-error` |

### 4. Reemplazar Clases de Cards

| ANTES | DESPUÉS |
|-------|---------|
| `card` (Bootstrap) | `card` (compatible) |
| `card-header` (Bootstrap) | `card-header` (compatible) |
| `card-body` (Bootstrap) | `card-body` (compatible) |
| `card-footer` (Bootstrap) | `card-footer` (compatible) |
| `card-title` (Bootstrap) | `card-title` (compatible) |

### 5. Reemplazar Clases de Tablas

| ANTES | DESPUÉS |
|-------|---------|
| `table` (Bootstrap) | `table` (compatible) |
| `table-striped` (Bootstrap) | Eliminar (ya incluido) |
| `table-hover` (Bootstrap) | Eliminar (ya incluido) |
| `table-responsive` (Bootstrap) | `table-container` |

### 6. Reemplazar Clases de Alertas

| ANTES | DESPUÉS |
|-------|---------|
| `alert alert-success` (Bootstrap) | `alert alert-success` (compatible) |
| `alert alert-danger` (Bootstrap) | `alert alert-error` |
| `alert alert-warning` (Bootstrap) | `alert alert-warning` (compatible) |
| `alert alert-info` (Bootstrap) | `alert alert-info` (compatible) |

### 7. Reemplazar Clases de Badges

| ANTES | DESPUÉS |
|-------|---------|
| `badge bg-success` (Bootstrap) | `badge badge-success` |
| `badge bg-danger` (Bootstrap) | `badge badge-error` |
| `badge bg-warning` (Bootstrap) | `badge badge-warning` |
| `badge bg-primary` (Bootstrap) | `badge badge-primary` |
| `badge bg-secondary` (Bootstrap) | `badge badge-secondary` |

### 8. Reemplazar Grid de Bootstrap

| ANTES | DESPUÉS |
|-------|---------|
| `<div class="row">` | `<div class="grid grid-cols-X">` |
| `<div class="col-md-6">` | `<div>` (dentro del grid) |
| `<div class="col-md-4">` | `<div>` (dentro del grid) |

**Ejemplo:**

**ANTES:**
```html
<div class="row">
    <div class="col-md-6">Columna 1</div>
    <div class="col-md-6">Columna 2</div>
</div>
```

**DESPUÉS:**
```html
<div class="grid grid-cols-2">
    <div>Columna 1</div>
    <div>Columna 2</div>
</div>
```

---

## 📝 EJEMPLOS DE MIGRACIÓN

### Ejemplo 1: Botón Simple

**ANTES:**
```html
<button class="btn btn-primary">Guardar</button>
```

**DESPUÉS:**
```html
<button class="btn btn-primary">
    <i class="fas fa-save"></i>
    Guardar
</button>
```

### Ejemplo 2: Formulario

**ANTES:**
```html
<div class="mb-3">
    <label for="nombre" class="form-label">Nombre</label>
    <input type="text" class="form-control" id="nombre">
</div>
```

**DESPUÉS:**
```html
<div class="form-group">
    <label for="nombre" class="form-label">Nombre</label>
    <input type="text" class="form-input" id="nombre">
</div>
```

### Ejemplo 3: Card

**ANTES:**
```html
<div class="card">
    <div class="card-header">
        <h5 class="card-title">Título</h5>
    </div>
    <div class="card-body">
        Contenido
    </div>
</div>
```

**DESPUÉS:**
```html
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Título</h3>
    </div>
    <div class="card-body">
        Contenido
    </div>
</div>
```

### Ejemplo 4: Tabla

**ANTES:**
```html
<div class="table-responsive">
    <table class="table table-striped table-hover">
        <thead>
            <tr>
                <th>Columna</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Dato</td>
            </tr>
        </tbody>
    </table>
</div>
```

**DESPUÉS:**
```html
<div class="table-container">
    <table class="table">
        <thead>
            <tr>
                <th>Columna</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Dato</td>
            </tr>
        </tbody>
    </table>
</div>
```

### Ejemplo 5: Badge

**ANTES:**
```html
<span class="badge bg-success">Activo</span>
<span class="badge bg-danger">Inactivo</span>
```

**DESPUÉS:**
```html
<span class="badge badge-success">Activo</span>
<span class="badge badge-error">Inactivo</span>
```

### Ejemplo 6: Alert

**ANTES:**
```html
<div class="alert alert-success">
    Operación exitosa
</div>
```

**DESPUÉS:**
```html
<div class="alert alert-success">
    <i class="fas fa-check-circle"></i>
    Operación exitosa
</div>
```

---

## 🎨 ESTILOS PERSONALIZADOS

### Eliminar Estilos Inline

**ANTES:**
```html
<div style="margin-top: 20px; padding: 15px; background: #fff;">
    Contenido
</div>
```

**DESPUÉS:**
```html
<div class="card mt-4">
    <div class="card-body">
        Contenido
    </div>
</div>
```

### Usar Variables CSS

**ANTES:**
```css
.mi-elemento {
    color: #41431B;
    background: #F8F3E1;
}
```

**DESPUÉS:**
```css
.mi-elemento {
    color: var(--color-primary);
    background: var(--color-background);
}
```

---

## 🔍 BUSCAR Y REEMPLAZAR

### Comandos de Búsqueda (VS Code)

1. **Buscar Bootstrap classes:**
   ```
   class="btn btn-primary"
   class="form-control"
   class="table-responsive"
   ```

2. **Reemplazar con nuevas classes:**
   ```
   class="btn btn-primary"  →  class="btn btn-primary"
   class="form-control"     →  class="form-input"
   class="table-responsive" →  class="table-container"
   ```

---

## ✅ CHECKLIST POR TEMPLATE

Para cada template, verifica:

- [ ] Actualizado el `<head>` con nuevo CSS
- [ ] Reemplazadas clases de botones
- [ ] Reemplazadas clases de formularios
- [ ] Reemplazadas clases de cards
- [ ] Reemplazadas clases de tablas
- [ ] Reemplazadas clases de alerts
- [ ] Reemplazadas clases de badges
- [ ] Convertido grid de Bootstrap a nuevo grid
- [ ] Eliminados estilos inline innecesarios
- [ ] Agregados íconos a botones
- [ ] Verificado responsive design
- [ ] Probado en navegador

---

## 📂 ORDEN DE MIGRACIÓN RECOMENDADO

### Prioridad Alta
1. ✅ `templates/base.html` - Template base principal
2. ✅ `templates/authentication/login.html` - Login
3. ✅ `templates/store/base_store.html` - Base de tienda
4. `templates/stock/product_list.html` - Lista de productos
5. `templates/stock/product_form.html` - Formulario de productos
6. `templates/customers/customer_list.html` - Lista de clientes
7. `templates/sales/pos.html` - Punto de venta

### Prioridad Media
8. `templates/suppliers/supplier_list.html`
9. `templates/suppliers/purchase_order_list.html`
10. `templates/reports/dashboard.html`
11. `templates/audit/audit_log.html`

### Prioridad Baja
12. Resto de templates de stock
13. Resto de templates de customers
14. Resto de templates de suppliers
15. Resto de templates de sales

---

## 🐛 PROBLEMAS COMUNES

### Problema 1: Botones sin estilo
**Causa:** Falta la clase `btn` base
**Solución:** Agregar `class="btn btn-primary"` en lugar de solo `class="btn-primary"`

### Problema 2: Inputs muy anchos
**Causa:** Falta el contenedor `form-group`
**Solución:** Envolver en `<div class="form-group">`

### Problema 3: Grid no responsive
**Causa:** Usando grid de Bootstrap
**Solución:** Cambiar a `<div class="grid grid-cols-X">` (se adapta automáticamente)

### Problema 4: Colores incorrectos
**Causa:** Usando colores hardcodeados
**Solución:** Usar variables CSS: `var(--color-primary)`

---

## 🚀 TESTING

Después de migrar cada template:

1. **Visual:** Verificar que se vea bien
2. **Responsive:** Probar en mobile, tablet, desktop
3. **Funcional:** Verificar que todos los botones funcionen
4. **Consistencia:** Comparar con otros templates migrados

---

## 📞 SOPORTE

Si encuentras problemas:
1. Revisa `SISTEMA_DISENO_UNIFICADO.md`
2. Compara con templates ya migrados
3. Verifica la consola del navegador (F12)

---

**Fecha:** 25 de Abril, 2026  
**Versión:** 1.0  
**Estado:** 📝 Guía Completa
