# 🎨 SISTEMA DE DISEÑO UNIFICADO - ROSS CRAFTS

## 📋 RESUMEN

Se ha creado un sistema de diseño completo y profesional que unifica todos los módulos del proyecto con:
- Paleta de colores consistente
- Tipografía moderna (Inter font)
- Componentes reutilizables
- Espaciado sistemático
- Responsive design
- Transiciones suaves

---

## 🎨 PALETA DE COLORES

### Colores Principales
```css
--color-primary: #41431B          /* Verde oscuro principal */
--color-primary-dark: #2d2f13     /* Verde más oscuro */
--color-primary-light: #5a5d26    /* Verde más claro */

--color-secondary: #AEB784        /* Verde medio */
--color-secondary-dark: #8a9468   /* Verde medio oscuro */
--color-secondary-light: #c5d19f  /* Verde medio claro */

--color-accent: #E3DBBB           /* Beige */
--color-background: #F8F3E1       /* Crema */
```

### Colores Semánticos
```css
--color-success: #10b981          /* Verde éxito */
--color-warning: #f59e0b          /* Naranja advertencia */
--color-error: #ef4444            /* Rojo error */
--color-info: #3b82f6             /* Azul información */
```

### Escala de Grises
```css
--color-gray-50: #f9fafb
--color-gray-100: #f3f4f6
--color-gray-200: #e5e7eb
--color-gray-300: #d1d5db
--color-gray-400: #9ca3af
--color-gray-500: #6b7280
--color-gray-600: #4b5563
--color-gray-700: #374151
--color-gray-800: #1f2937
--color-gray-900: #111827
```

---

## 📝 TIPOGRAFÍA

### Fuente
**Inter** - Fuente moderna, legible y profesional
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Tamaños
```css
--font-size-xs: 0.75rem      /* 12px */
--font-size-sm: 0.875rem     /* 14px */
--font-size-base: 1rem       /* 16px */
--font-size-lg: 1.125rem     /* 18px */
--font-size-xl: 1.25rem      /* 20px */
--font-size-2xl: 1.5rem      /* 24px */
--font-size-3xl: 1.875rem    /* 30px */
--font-size-4xl: 2.25rem     /* 36px */
--font-size-5xl: 3rem        /* 48px */
```

### Pesos
```css
--font-weight-normal: 400
--font-weight-medium: 500
--font-weight-semibold: 600
--font-weight-bold: 700
```

### Jerarquía de Títulos
```html
<h1>Título Principal</h1>      <!-- 36px, bold -->
<h2>Título Secundario</h2>     <!-- 30px, bold -->
<h3>Título Terciario</h3>      <!-- 24px, bold -->
<h4>Título Cuaternario</h4>    <!-- 20px, bold -->
<h5>Título Quinario</h5>       <!-- 18px, bold -->
<h6>Título Sexto</h6>          <!-- 16px, bold -->
```

---

## 🔘 BOTONES

### Estructura Base
```html
<button class="btn btn-primary">Botón</button>
```

### Variantes
```html
<!-- Primario -->
<button class="btn btn-primary">Primario</button>

<!-- Secundario -->
<button class="btn btn-secondary">Secundario</button>

<!-- Éxito -->
<button class="btn btn-success">Éxito</button>

<!-- Advertencia -->
<button class="btn btn-warning">Advertencia</button>

<!-- Error -->
<button class="btn btn-error">Error</button>

<!-- Outline -->
<button class="btn btn-outline">Outline</button>

<!-- Ghost -->
<button class="btn btn-ghost">Ghost</button>
```

### Tamaños
```html
<button class="btn btn-primary btn-xs">Extra Pequeño</button>
<button class="btn btn-primary btn-sm">Pequeño</button>
<button class="btn btn-primary">Normal</button>
<button class="btn btn-primary btn-lg">Grande</button>
<button class="btn btn-primary btn-xl">Extra Grande</button>
```

### Con Íconos
```html
<button class="btn btn-primary">
    <i class="fas fa-save"></i>
    Guardar
</button>
```

### Deshabilitado
```html
<button class="btn btn-primary" disabled>Deshabilitado</button>
```

---

## 📝 FORMULARIOS

### Input Básico
```html
<div class="form-group">
    <label for="nombre" class="form-label">Nombre</label>
    <input type="text" id="nombre" class="form-input" placeholder="Ingresa tu nombre">
</div>
```

### Input Requerido
```html
<div class="form-group">
    <label for="email" class="form-label form-label-required">Email</label>
    <input type="email" id="email" class="form-input" required>
</div>
```

### Select
```html
<div class="form-group">
    <label for="categoria" class="form-label">Categoría</label>
    <select id="categoria" class="form-select">
        <option>Opción 1</option>
        <option>Opción 2</option>
    </select>
</div>
```

### Textarea
```html
<div class="form-group">
    <label for="descripcion" class="form-label">Descripción</label>
    <textarea id="descripcion" class="form-textarea"></textarea>
</div>
```

### Con Ayuda
```html
<div class="form-group">
    <label for="password" class="form-label">Contraseña</label>
    <input type="password" id="password" class="form-input">
    <span class="form-help">Mínimo 8 caracteres</span>
</div>
```

### Con Error
```html
<div class="form-group">
    <label for="email" class="form-label">Email</label>
    <input type="email" id="email" class="form-input is-invalid">
    <span class="form-error">Email inválido</span>
</div>
```

---

## 🃏 CARDS

### Card Básica
```html
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Título de la Card</h3>
    </div>
    <div class="card-body">
        <p>Contenido de la card</p>
    </div>
    <div class="card-footer">
        <button class="btn btn-primary">Acción</button>
    </div>
</div>
```

### Card Simple
```html
<div class="card">
    <div class="card-body">
        <h3>Título</h3>
        <p>Contenido</p>
    </div>
</div>
```

---

## 📊 TABLAS

### Tabla Básica
```html
<div class="table-container">
    <table class="table">
        <thead>
            <tr>
                <th>Columna 1</th>
                <th>Columna 2</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Dato 1</td>
                <td>Dato 2</td>
                <td>
                    <button class="btn btn-sm btn-primary">Editar</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

---

## 🏷️ BADGES

### Badges Básicos
```html
<span class="badge badge-primary">Primario</span>
<span class="badge badge-secondary">Secundario</span>
<span class="badge badge-success">Éxito</span>
<span class="badge badge-warning">Advertencia</span>
<span class="badge badge-error">Error</span>
<span class="badge badge-info">Info</span>
<span class="badge badge-gray">Gris</span>
```

### Uso en Tablas
```html
<td>
    <span class="badge badge-success">Activo</span>
</td>
<td>
    <span class="badge badge-error">Inactivo</span>
</td>
```

---

## 🚨 ALERTAS

### Alertas
```html
<!-- Éxito -->
<div class="alert alert-success">
    <i class="fas fa-check-circle"></i>
    Operación exitosa
</div>

<!-- Advertencia -->
<div class="alert alert-warning">
    <i class="fas fa-exclamation-triangle"></i>
    Ten cuidado
</div>

<!-- Error -->
<div class="alert alert-error">
    <i class="fas fa-times-circle"></i>
    Ocurrió un error
</div>

<!-- Info -->
<div class="alert alert-info">
    <i class="fas fa-info-circle"></i>
    Información importante
</div>
```

---

## 📐 ESPACIADO

### Sistema de Espaciado
```css
--spacing-xs: 0.25rem    /* 4px */
--spacing-sm: 0.5rem     /* 8px */
--spacing-md: 1rem       /* 16px */
--spacing-lg: 1.5rem     /* 24px */
--spacing-xl: 2rem       /* 32px */
--spacing-2xl: 3rem      /* 48px */
--spacing-3xl: 4rem      /* 64px */
```

### Clases de Utilidad
```html
<!-- Margin Top -->
<div class="mt-0">Sin margen superior</div>
<div class="mt-1">Margen superior xs</div>
<div class="mt-2">Margen superior sm</div>
<div class="mt-3">Margen superior md</div>
<div class="mt-4">Margen superior lg</div>
<div class="mt-5">Margen superior xl</div>

<!-- Margin Bottom -->
<div class="mb-0">Sin margen inferior</div>
<div class="mb-1">Margen inferior xs</div>
<div class="mb-2">Margen inferior sm</div>
<div class="mb-3">Margen inferior md</div>
<div class="mb-4">Margen inferior lg</div>
<div class="mb-5">Margen inferior xl</div>
```

---

## 🎯 LAYOUT

### Container
```html
<div class="container">
    <!-- Contenido con ancho máximo de 1400px -->
</div>
```

### Page Header
```html
<div class="page-header">
    <h1 class="page-title">Título de la Página</h1>
    <p class="page-subtitle">Subtítulo o descripción</p>
</div>
```

### Grid System
```html
<!-- 2 columnas -->
<div class="grid grid-cols-2">
    <div>Columna 1</div>
    <div>Columna 2</div>
</div>

<!-- 3 columnas -->
<div class="grid grid-cols-3">
    <div>Columna 1</div>
    <div>Columna 2</div>
    <div>Columna 3</div>
</div>

<!-- 4 columnas -->
<div class="grid grid-cols-4">
    <div>Columna 1</div>
    <div>Columna 2</div>
    <div>Columna 3</div>
    <div>Columna 4</div>
</div>
```

---

## 🎨 NAVBAR

### Navbar del Dashboard
```html
<nav class="navbar">
    <div class="navbar-container">
        <a href="/" class="navbar-brand">
            <i class="fas fa-palette"></i>
            Ross Crafts
        </a>
        
        <div class="navbar-menu">
            <a href="#" class="navbar-link">
                <i class="fas fa-home"></i> Inicio
            </a>
            <a href="#" class="navbar-link active">
                <i class="fas fa-box"></i> Productos
            </a>
            <a href="#" class="navbar-link">
                <i class="fas fa-users"></i> Clientes
            </a>
        </div>
    </div>
</nav>
```

---

## 🔧 UTILIDADES

### Texto
```html
<!-- Alineación -->
<p class="text-left">Izquierda</p>
<p class="text-center">Centro</p>
<p class="text-right">Derecha</p>

<!-- Colores -->
<p class="text-primary">Primario</p>
<p class="text-secondary">Secundario</p>
<p class="text-success">Éxito</p>
<p class="text-warning">Advertencia</p>
<p class="text-error">Error</p>
<p class="text-gray">Gris</p>

<!-- Tamaños -->
<p class="text-xs">Extra pequeño</p>
<p class="text-sm">Pequeño</p>
<p class="text-base">Normal</p>
<p class="text-lg">Grande</p>
<p class="text-xl">Extra grande</p>

<!-- Pesos -->
<p class="font-normal">Normal</p>
<p class="font-medium">Medio</p>
<p class="font-semibold">Semi-negrita</p>
<p class="font-bold">Negrita</p>
```

### Flexbox
```html
<div class="flex items-center justify-between">
    <div>Izquierda</div>
    <div>Derecha</div>
</div>

<div class="flex items-center gap-3">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
```

---

## 📱 RESPONSIVE

### Breakpoints
```css
/* Mobile: < 768px */
/* Tablet: 768px - 1024px */
/* Desktop: > 1024px */
```

### Comportamiento
- **Grid:** 4 columnas → 2 columnas → 1 columna
- **Navbar:** Completo → Completo → Hamburger
- **Tablas:** Scroll horizontal en mobile
- **Cards:** Stack vertical en mobile

---

## 🎯 EJEMPLOS DE USO

### Página de Lista
```html
{% extends 'base.html' %}

{% block content %}
<div class="page-header">
    <h1 class="page-title">Productos</h1>
    <p class="page-subtitle">Gestiona tu catálogo de productos</p>
</div>

<div class="card">
    <div class="card-header">
        <h3 class="card-title">Lista de Productos</h3>
    </div>
    <div class="card-body">
        <div class="table-container">
            <table class="table">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Precio</th>
                        <th>Stock</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Producto 1</td>
                        <td>S/. 50.00</td>
                        <td>10</td>
                        <td><span class="badge badge-success">Activo</span></td>
                        <td>
                            <button class="btn btn-sm btn-primary">
                                <i class="fas fa-edit"></i> Editar
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

### Formulario
```html
{% extends 'base.html' %}

{% block content %}
<div class="page-header">
    <h1 class="page-title">Nuevo Producto</h1>
</div>

<div class="card">
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            
            <div class="grid grid-cols-2">
                <div class="form-group">
                    <label for="nombre" class="form-label form-label-required">Nombre</label>
                    <input type="text" id="nombre" name="nombre" class="form-input" required>
                </div>
                
                <div class="form-group">
                    <label for="precio" class="form-label form-label-required">Precio</label>
                    <input type="number" id="precio" name="precio" class="form-input" step="0.01" required>
                </div>
            </div>
            
            <div class="form-group">
                <label for="descripcion" class="form-label">Descripción</label>
                <textarea id="descripcion" name="descripcion" class="form-textarea"></textarea>
            </div>
            
            <div class="flex justify-end gap-3">
                <a href="{% url 'product_list' %}" class="btn btn-outline">Cancelar</a>
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-save"></i> Guardar
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Para Cada Módulo

- [ ] Actualizar template para usar `design-system.css`
- [ ] Reemplazar botones con clases `.btn`
- [ ] Usar `.card` para contenedores
- [ ] Aplicar `.table` a tablas
- [ ] Usar `.badge` para estados
- [ ] Aplicar `.alert` para mensajes
- [ ] Usar `.form-group`, `.form-label`, `.form-input`
- [ ] Aplicar `.page-header` y `.page-title`
- [ ] Usar grid system para layouts
- [ ] Verificar responsive design

---

## 🚀 PRÓXIMOS PASOS

1. Actualizar todos los templates de productos
2. Actualizar todos los templates de clientes
3. Actualizar todos los templates de proveedores
4. Actualizar todos los templates de ventas
5. Actualizar todos los templates de reportes
6. Actualizar todos los templates de auditoría
7. Verificar consistencia en toda la aplicación
8. Testing en diferentes dispositivos

---

**Fecha:** 25 de Abril, 2026  
**Versión:** 1.0  
**Estado:** ✅ Sistema de Diseño Creado
