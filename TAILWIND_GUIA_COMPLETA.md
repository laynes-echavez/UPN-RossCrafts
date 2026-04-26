# 🎨 GUÍA COMPLETA DE TAILWIND CSS - ROSS CRAFTS

## 📋 RESUMEN

Se ha implementado Tailwind CSS en el proyecto para lograr:
- Diseño consistente y profesional
- Desarrollo rápido
- Responsive design automático
- Mantenibilidad mejorada

---

## 🚀 CONFIGURACIÓN

### Colores Personalizados

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#41431B',
                    dark: '#2d2f13',
                    light: '#5a5d26',
                },
                secondary: {
                    DEFAULT: '#AEB784',
                    dark: '#8a9468',
                    light: '#c5d19f',
                },
                accent: '#E3DBBB',
                cream: '#F8F3E1',
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        }
    }
}
```

### Incluir en Templates

```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Configuración -->
<script>
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    primary: {
                        DEFAULT: '#41431B',
                        dark: '#2d2f13',
                        light: '#5a5d26',
                    },
                    secondary: {
                        DEFAULT: '#AEB784',
                        dark: '#8a9468',
                        light: '#c5d19f',
                    },
                    accent: '#E3DBBB',
                    cream: '#F8F3E1',
                },
            }
        }
    }
</script>
```

---

## 🎨 COMPONENTES COMUNES

### 1. BOTONES

#### Botón Primario
```html
<button class="bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-4 rounded-lg transition duration-200 flex items-center space-x-2">
    <i class="fas fa-save"></i>
    <span>Guardar</span>
</button>
```

#### Botón Secundario
```html
<button class="bg-secondary hover:bg-secondary-dark text-white font-semibold py-2 px-4 rounded-lg transition duration-200">
    Cancelar
</button>
```

#### Botón Outline
```html
<button class="border-2 border-primary text-primary hover:bg-primary hover:text-white font-semibold py-2 px-4 rounded-lg transition duration-200">
    Ver Más
</button>
```

#### Botón Peligro
```html
<button class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200">
    <i class="fas fa-trash"></i>
    Eliminar
</button>
```

#### Botón Éxito
```html
<button class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200">
    <i class="fas fa-check"></i>
    Confirmar
</button>
```

#### Tamaños
```html
<!-- Pequeño -->
<button class="bg-primary text-white py-1 px-3 text-sm rounded-lg">Pequeño</button>

<!-- Normal -->
<button class="bg-primary text-white py-2 px-4 rounded-lg">Normal</button>

<!-- Grande -->
<button class="bg-primary text-white py-3 px-6 text-lg rounded-lg">Grande</button>
```

### 2. FORMULARIOS

#### Input de Texto
```html
<div class="mb-4">
    <label for="nombre" class="block text-sm font-medium text-gray-700 mb-2">
        Nombre <span class="text-red-500">*</span>
    </label>
    <input 
        type="text" 
        id="nombre" 
        name="nombre"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition"
        placeholder="Ingresa el nombre"
        required
    >
</div>
```

#### Input con Ícono
```html
<div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
    <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <i class="fas fa-envelope text-gray-400"></i>
        </div>
        <input 
            type="email"
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            placeholder="correo@ejemplo.com"
        >
    </div>
</div>
```

#### Select
```html
<div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-2">Categoría</label>
    <select class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
        <option>Selecciona una opción</option>
        <option>Opción 1</option>
        <option>Opción 2</option>
    </select>
</div>
```

#### Textarea
```html
<div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
    <textarea 
        rows="4"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
        placeholder="Escribe una descripción..."
    ></textarea>
</div>
```

#### Checkbox
```html
<div class="flex items-center mb-4">
    <input 
        type="checkbox" 
        id="activo"
        class="w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary"
    >
    <label for="activo" class="ml-2 text-sm text-gray-700">Activo</label>
</div>
```

### 3. CARDS

#### Card Básica
```html
<div class="bg-white rounded-lg shadow-md overflow-hidden">
    <div class="p-6">
        <h3 class="text-xl font-bold text-primary mb-2">Título</h3>
        <p class="text-gray-600">Contenido de la card</p>
    </div>
</div>
```

#### Card con Header y Footer
```html
<div class="bg-white rounded-lg shadow-md overflow-hidden">
    <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-primary">Título de la Card</h3>
    </div>
    <div class="p-6">
        <p class="text-gray-600">Contenido principal</p>
    </div>
    <div class="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
        <button class="bg-gray-200 hover:bg-gray-300 text-gray-700 py-2 px-4 rounded-lg transition">
            Cancelar
        </button>
        <button class="bg-primary hover:bg-primary-dark text-white py-2 px-4 rounded-lg transition">
            Guardar
        </button>
    </div>
</div>
```

#### Card con Hover
```html
<div class="bg-white rounded-lg shadow-md hover:shadow-xl transition duration-300 transform hover:-translate-y-1 overflow-hidden cursor-pointer">
    <div class="p-6">
        <h3 class="text-xl font-bold text-primary mb-2">Producto</h3>
        <p class="text-gray-600 mb-4">Descripción del producto</p>
        <span class="text-2xl font-bold text-primary">S/. 50.00</span>
    </div>
</div>
```

### 4. TABLAS

#### Tabla Básica
```html
<div class="overflow-x-auto bg-white rounded-lg shadow-md">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-primary">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                    Nombre
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                    Precio
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                    Stock
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                    Acciones
                </th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            <tr class="hover:bg-gray-50 transition">
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">Producto 1</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">S/. 50.00</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        10 unidades
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button class="text-blue-600 hover:text-blue-900">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="text-red-600 hover:text-red-900">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### 5. BADGES

```html
<!-- Éxito -->
<span class="px-3 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
    Activo
</span>

<!-- Error -->
<span class="px-3 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800">
    Inactivo
</span>

<!-- Advertencia -->
<span class="px-3 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
    Pendiente
</span>

<!-- Info -->
<span class="px-3 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
    En proceso
</span>

<!-- Primario -->
<span class="px-3 py-1 text-xs font-semibold rounded-full bg-primary text-white">
    Destacado
</span>
```

### 6. ALERTAS

```html
<!-- Éxito -->
<div class="bg-green-50 border border-green-200 text-green-800 rounded-lg p-4 flex items-start space-x-3">
    <i class="fas fa-check-circle text-xl"></i>
    <span class="flex-1">Operación completada exitosamente</span>
</div>

<!-- Error -->
<div class="bg-red-50 border border-red-200 text-red-800 rounded-lg p-4 flex items-start space-x-3">
    <i class="fas fa-times-circle text-xl"></i>
    <span class="flex-1">Ocurrió un error al procesar la solicitud</span>
</div>

<!-- Advertencia -->
<div class="bg-yellow-50 border border-yellow-200 text-yellow-800 rounded-lg p-4 flex items-start space-x-3">
    <i class="fas fa-exclamation-triangle text-xl"></i>
    <span class="flex-1">Ten cuidado con esta acción</span>
</div>

<!-- Info -->
<div class="bg-blue-50 border border-blue-200 text-blue-800 rounded-lg p-4 flex items-start space-x-3">
    <i class="fas fa-info-circle text-xl"></i>
    <span class="flex-1">Información importante</span>
</div>
```

### 7. MODALES

```html
<!-- Overlay -->
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <!-- Modal -->
    <div class="bg-white rounded-lg shadow-2xl max-w-md w-full mx-4">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
            <h3 class="text-xl font-bold text-primary">Título del Modal</h3>
            <button class="text-gray-400 hover:text-gray-600 transition">
                <i class="fas fa-times text-xl"></i>
            </button>
        </div>
        
        <!-- Body -->
        <div class="p-6">
            <p class="text-gray-600">Contenido del modal</p>
        </div>
        
        <!-- Footer -->
        <div class="flex justify-end space-x-3 p-6 border-t border-gray-200">
            <button class="bg-gray-200 hover:bg-gray-300 text-gray-700 py-2 px-4 rounded-lg transition">
                Cancelar
            </button>
            <button class="bg-primary hover:bg-primary-dark text-white py-2 px-4 rounded-lg transition">
                Confirmar
            </button>
        </div>
    </div>
</div>
```

---

## 📐 LAYOUTS

### Grid de 2 Columnas
```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>Columna 1</div>
    <div>Columna 2</div>
</div>
```

### Grid de 3 Columnas
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div>Columna 1</div>
    <div>Columna 2</div>
    <div>Columna 3</div>
</div>
```

### Grid de 4 Columnas
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
    <div>Columna 1</div>
    <div>Columna 2</div>
    <div>Columna 3</div>
    <div>Columna 4</div>
</div>
```

### Flex con Espacio Entre
```html
<div class="flex items-center justify-between">
    <div>Izquierda</div>
    <div>Derecha</div>
</div>
```

---

## 🎯 EJEMPLOS COMPLETOS

### Página de Lista
```html
{% extends 'base.html' %}

{% block content %}
<!-- Header -->
<div class="mb-8">
    <div class="flex items-center justify-between">
        <div>
            <h1 class="text-3xl font-bold text-primary">Productos</h1>
            <p class="text-gray-600 mt-1">Gestiona tu catálogo de productos</p>
        </div>
        <a href="{% url 'product_create' %}" class="bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-4 rounded-lg transition flex items-center space-x-2">
            <i class="fas fa-plus"></i>
            <span>Nuevo Producto</span>
        </a>
    </div>
</div>

<!-- Filtros -->
<div class="bg-white rounded-lg shadow-md p-6 mb-6">
    <form method="get" class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <input 
            type="text" 
            name="search" 
            placeholder="Buscar..."
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
        >
        <select name="category" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
            <option value="">Todas las categorías</option>
        </select>
        <select name="status" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
            <option value="">Todos los estados</option>
            <option value="active">Activo</option>
            <option value="inactive">Inactivo</option>
        </select>
        <button type="submit" class="bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-4 rounded-lg transition">
            <i class="fas fa-search mr-2"></i>
            Buscar
        </button>
    </form>
</div>

<!-- Tabla -->
<div class="bg-white rounded-lg shadow-md overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-primary">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase">Nombre</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase">Precio</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase">Stock</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase">Estado</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase">Acciones</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for product in products %}
            <tr class="hover:bg-gray-50 transition">
                <td class="px-6 py-4">{{ product.name }}</td>
                <td class="px-6 py-4">S/. {{ product.price }}</td>
                <td class="px-6 py-4">{{ product.stock }}</td>
                <td class="px-6 py-4">
                    <span class="px-3 py-1 text-xs font-semibold rounded-full {% if product.is_active %}bg-green-100 text-green-800{% else %}bg-red-100 text-red-800{% endif %}">
                        {% if product.is_active %}Activo{% else %}Inactivo{% endif %}
                    </span>
                </td>
                <td class="px-6 py-4 space-x-2">
                    <a href="{% url 'product_edit' product.pk %}" class="text-blue-600 hover:text-blue-900">
                        <i class="fas fa-edit"></i>
                    </a>
                    <a href="{% url 'product_delete' product.pk %}" class="text-red-600 hover:text-red-900">
                        <i class="fas fa-trash"></i>
                    </a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

### Formulario
```html
{% extends 'base.html' %}

{% block content %}
<div class="max-w-3xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-primary">Nuevo Producto</h1>
        <p class="text-gray-600 mt-1">Completa los datos del producto</p>
    </div>

    <!-- Formulario -->
    <div class="bg-white rounded-lg shadow-md p-8">
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                        Nombre <span class="text-red-500">*</span>
                    </label>
                    <input 
                        type="text" 
                        name="name"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        required
                    >
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                        SKU <span class="text-red-500">*</span>
                    </label>
                    <input 
                        type="text" 
                        name="sku"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        required
                    >
                </div>
            </div>
            
            <div class="mt-6">
                <label class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
                <textarea 
                    name="description"
                    rows="4"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
                ></textarea>
            </div>
            
            <div class="flex justify-end space-x-3 mt-8">
                <a href="{% url 'product_list' %}" class="border-2 border-gray-300 text-gray-700 hover:bg-gray-50 font-semibold py-2 px-6 rounded-lg transition">
                    Cancelar
                </a>
                <button type="submit" class="bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-6 rounded-lg transition flex items-center space-x-2">
                    <i class="fas fa-save"></i>
                    <span>Guardar</span>
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

---

## 📱 RESPONSIVE

### Breakpoints de Tailwind
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

### Ejemplos
```html
<!-- Ocultar en mobile, mostrar en desktop -->
<div class="hidden md:block">Visible solo en desktop</div>

<!-- Mostrar en mobile, ocultar en desktop -->
<div class="block md:hidden">Visible solo en mobile</div>

<!-- Tamaño de texto responsive -->
<h1 class="text-2xl md:text-3xl lg:text-4xl">Título Responsive</h1>

<!-- Padding responsive -->
<div class="p-4 md:p-6 lg:p-8">Contenido</div>

<!-- Grid responsive -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- Items -->
</div>
```

---

## ✅ CHECKLIST DE MIGRACIÓN

Para cada template:

- [ ] Incluir Tailwind CSS CDN
- [ ] Incluir configuración de colores
- [ ] Reemplazar clases de Bootstrap
- [ ] Usar colores personalizados (primary, secondary)
- [ ] Agregar transiciones (transition, duration-200)
- [ ] Hacer responsive (md:, lg:)
- [ ] Agregar hover effects
- [ ] Usar espaciado consistente (p-4, m-4, space-x-2)
- [ ] Probar en mobile, tablet, desktop

---

**Fecha:** 25 de Abril, 2026  
**Versión:** 1.0  
**Estado:** ✅ Guía Completa
