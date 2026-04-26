# 🗺️ GUÍA DE NAVEGACIÓN COMPLETA - ROSS CRAFTS

## 📍 MAPA DEL SISTEMA

Ross Crafts tiene **DOS INTERFACES PRINCIPALES** completamente integradas:

### 1. 🏪 TIENDA ONLINE (Pública)
**Acceso:** http://127.0.0.1:8000/
**Para:** Clientes y visitantes

### 2. 💼 DASHBOARD (Privado)
**Acceso:** http://127.0.0.1:8000/auth/login/
**Para:** Empleados, administradores y gerentes

---

## 🏪 NAVEGACIÓN EN LA TIENDA ONLINE

### Estructura de la Tienda

```
TIENDA ONLINE
│
├── 🏠 INICIO (/)
│   ├── Hero Banner con búsqueda
│   ├── Categorías destacadas
│   ├── Productos destacados
│   └── Características del servicio
│
├── 🛍️ CATÁLOGO (/tienda/)
│   ├── Filtros laterales
│   │   ├── Por categoría
│   │   ├── Por rango de precio
│   │   └── Por disponibilidad
│   ├── Ordenamiento
│   ├── Grid de productos
│   └── Paginación
│
├── 📦 DETALLE DE PRODUCTO (/tienda/<slug>/)
│   ├── Imagen grande
│   ├── Información completa
│   ├── Selector de cantidad
│   ├── Botón agregar al carrito
│   └── Productos relacionados
│
└── 🛒 CARRITO (/carrito/)
    ├── Lista de productos
    ├── Actualizar cantidades
    ├── Eliminar productos
    ├── Resumen del pedido
    └── Proceder al pago (próximamente)
```

### Navbar de la Tienda

**Para Visitantes (No autenticados):**
```
[Ross Crafts] [Inicio] [Tienda] [Iniciar Sesión] [🛒 Carrito (N)]
```

**Para Usuarios Autenticados:**
```
[Ross Crafts] [Inicio] [Tienda] [👤 Usuario ▼] [🛒 Carrito (N)]
                                      │
                                      ├── Dashboard
                                      └── Cerrar Sesión
```

---

## 💼 NAVEGACIÓN EN EL DASHBOARD

### Estructura del Dashboard

```
DASHBOARD
│
├── 🔐 LOGIN (/auth/login/)
│   └── Redirige según rol después del login
│
├── 📊 DASHBOARD PRINCIPAL (/auth/dashboard/)
│   ├── Gerente → Reportes
│   ├── Administrador → POS
│   └── Empleado → POS
│
├── 📦 GESTIÓN DE PRODUCTOS
│   ├── /stock/ - Lista de productos
│   ├── /stock/nuevo/ - Crear producto
│   ├── /stock/<id>/editar/ - Editar producto
│   ├── /stock/<id>/detalle/ - Ver detalle
│   ├── /stock/movimientos/ - Movimientos de stock
│   └── /stock/categorias/ - Gestión de categorías
│
├── 👥 GESTIÓN DE CLIENTES
│   ├── /clientes/ - Lista de clientes
│   ├── /clientes/nuevo/ - Crear cliente
│   ├── /clientes/<id>/editar/ - Editar cliente
│   ├── /clientes/<id>/perfil/ - Ver perfil
│   └── /clientes/exportar/ - Exportar a Excel
│
├── 🏭 GESTIÓN DE PROVEEDORES
│   ├── /proveedores/ - Lista de proveedores
│   ├── /proveedores/nuevo/ - Crear proveedor
│   ├── /proveedores/<id>/editar/ - Editar proveedor
│   ├── /proveedores/<id>/detalle/ - Ver detalle
│   ├── /compras/ - Órdenes de compra
│   ├── /compras/nueva/ - Nueva orden
│   ├── /compras/<id>/detalle/ - Ver orden
│   ├── /compras/<id>/recibir/ - Marcar como recibida
│   └── /compras/exportar/ - Exportar a Excel
│
├── 💰 PUNTO DE VENTA (POS)
│   └── /pos/ - Sistema de ventas presenciales
│       ├── Búsqueda de productos
│       ├── Gestión de carrito
│       ├── Registro de cliente rápido
│       ├── Aplicar descuentos
│       └── Generar recibo PDF
│
├── 📈 REPORTES (Solo Gerente)
│   └── /reports/ - Dashboard de reportes
│
└── 🛡️ AUDITORÍA (Solo Gerente)
    └── /dashboard/auditoria/ - Log de auditoría
```

### Navbar del Dashboard

**Para Todos los Usuarios Autenticados:**
```
[Ross Crafts] [Dashboard] [🏪 Tienda Online] [Productos] [Stock] [POS] [Cerrar Sesión]
```

**Para Gerente (adicional):**
```
[...] [🛡️ Auditoría] [...]
```

---

## 🔄 FLUJOS DE NAVEGACIÓN COMUNES

### Flujo 1: Cliente Comprando en la Tienda

```
1. Visitante entra a la tienda (/)
   ↓
2. Explora categorías o busca productos
   ↓
3. Va al catálogo (/tienda/)
   ↓
4. Aplica filtros y encuentra producto
   ↓
5. Hace clic en producto → Detalle (/tienda/<slug>/)
   ↓
6. Ajusta cantidad y agrega al carrito
   ↓
7. Contador del carrito se actualiza (🛒 1)
   ↓
8. Continúa comprando o va al carrito (/carrito/)
   ↓
9. Revisa productos, ajusta cantidades
   ↓
10. Procede al pago (próximamente)
```

### Flujo 2: Empleado Vendiendo en POS

```
1. Empleado inicia sesión (/auth/login/)
   ↓
2. Redirige automáticamente al POS (/pos/)
   ↓
3. Busca productos por nombre/SKU
   ↓
4. Agrega productos al carrito
   ↓
5. Busca cliente existente o registra uno nuevo
   ↓
6. Aplica descuento si es necesario
   ↓
7. Selecciona método de pago
   ↓
8. Registra la venta
   ↓
9. Genera e imprime recibo PDF
   ↓
10. Stock se actualiza automáticamente
```

### Flujo 3: Administrador Gestionando Productos

```
1. Admin inicia sesión (/auth/login/)
   ↓
2. Va a Productos (/stock/)
   ↓
3. Crea nuevo producto (/stock/nuevo/)
   ↓
4. Sube imagen, define precio, stock, etc.
   ↓
5. Guarda producto
   ↓
6. Producto aparece automáticamente en la tienda
   ↓
7. Puede editar desde /stock/<id>/editar/
   ↓
8. Puede ver movimientos de stock
   ↓
9. Puede importar productos desde Excel
```

### Flujo 4: Gerente Recibiendo Orden de Compra

```
1. Gerente inicia sesión (/auth/login/)
   ↓
2. Va a Proveedores → Órdenes de Compra (/compras/)
   ↓
3. Crea nueva orden (/compras/nueva/)
   ↓
4. Selecciona proveedor
   ↓
5. Agrega productos con cantidades y costos
   ↓
6. Guarda orden (estado: Pendiente)
   ↓
7. Cuando llega la mercancía, va a detalle (/compras/<id>/detalle/)
   ↓
8. Hace clic en "Marcar como Recibida"
   ↓
9. Stock se actualiza automáticamente
   ↓
10. Se crean movimientos de stock tipo "entrada"
```

### Flujo 5: Usuario Navegando Entre Tienda y Dashboard

```
DESDE DASHBOARD → TIENDA:
Dashboard → Clic en "🏪 Tienda Online" → Abre en nueva pestaña

DESDE TIENDA → DASHBOARD:
Tienda → Clic en "👤 Usuario" → "Dashboard" → Redirige según rol
```

---

## 🎯 ACCESOS RÁPIDOS

### URLs Directas Importantes

#### Tienda Online
- **Inicio:** http://127.0.0.1:8000/
- **Catálogo:** http://127.0.0.1:8000/tienda/
- **Carrito:** http://127.0.0.1:8000/carrito/

#### Dashboard
- **Login:** http://127.0.0.1:8000/auth/login/
- **POS:** http://127.0.0.1:8000/pos/
- **Productos:** http://127.0.0.1:8000/stock/
- **Clientes:** http://127.0.0.1:8000/clientes/
- **Proveedores:** http://127.0.0.1:8000/proveedores/
- **Órdenes de Compra:** http://127.0.0.1:8000/compras/
- **Auditoría:** http://127.0.0.1:8000/dashboard/auditoria/

---

## 🔐 PERMISOS POR ROL

### Gerente (Acceso Total)
✅ Ver y gestionar productos
✅ Ver y gestionar clientes
✅ Ver y gestionar proveedores
✅ Crear y recibir órdenes de compra
✅ Cancelar órdenes de compra
✅ Usar POS
✅ Ver reportes
✅ Ver auditoría
✅ Eliminar/desactivar registros

### Administrador
✅ Ver y gestionar productos
✅ Ver y gestionar clientes
✅ Ver y gestionar proveedores
✅ Crear órdenes de compra
✅ Recibir órdenes de compra
✅ Usar POS
❌ Ver reportes
❌ Ver auditoría
❌ Cancelar órdenes de compra

### Empleado
✅ Ver productos
✅ Ver y crear clientes
✅ Usar POS
❌ Gestionar productos
❌ Gestionar proveedores
❌ Órdenes de compra
❌ Ver reportes
❌ Ver auditoría

---

## 🎨 DIFERENCIAS VISUALES

### Tienda Online
- **Fondo:** Crema (#F8F3E1)
- **Navbar:** Verde oscuro (#41431B)
- **Estilo:** Moderno, limpio, orientado al cliente
- **Tipografía:** Segoe UI, sans-serif
- **Imágenes:** Grandes, destacadas
- **Botones:** Redondeados, con efectos hover

### Dashboard
- **Fondo:** Blanco/gris claro
- **Navbar:** Verde oscuro (#41431B)
- **Estilo:** Funcional, orientado a la gestión
- **Tipografía:** System fonts
- **Tablas:** Compactas, con filtros
- **Botones:** Rectangulares, colores semánticos

---

## 📱 RESPONSIVE

### Tienda Online
- **Desktop:** 3 columnas de productos, sidebar sticky
- **Tablet:** 2 columnas, sidebar sticky
- **Mobile:** 1 columna, hamburger menu

### Dashboard
- **Desktop:** Tablas completas, sidebar visible
- **Tablet:** Tablas con scroll horizontal
- **Mobile:** Tablas apiladas, menú colapsable

---

## 🔍 BÚSQUEDA Y FILTROS

### En la Tienda
- **Búsqueda:** Por nombre, descripción, SKU
- **Filtros:** Categoría, precio, disponibilidad
- **Ordenamiento:** Nombre, precio, fecha

### En el Dashboard
- **Productos:** Nombre, SKU, categoría, stock
- **Clientes:** Nombre, DNI, email, estado
- **Proveedores:** Nombre, RUC, estado
- **Órdenes:** Proveedor, estado, fechas

---

## 💡 TIPS DE NAVEGACIÓN

### Para Clientes
1. Usa la búsqueda del hero banner para encontrar rápido
2. Filtra por categoría para explorar productos similares
3. El contador del carrito siempre muestra cuántos items tienes
4. Puedes ajustar cantidades directamente en el carrito
5. Inicia sesión para que tu carrito persista entre sesiones

### Para Empleados
1. El POS es tu pantalla principal tras login
2. Usa búsqueda rápida de productos con Enter
3. Registra clientes rápidamente sin salir del POS
4. El stock se actualiza automáticamente al vender
5. Imprime recibos directamente desde el navegador

### Para Administradores
1. Importa productos masivamente desde Excel
2. Exporta clientes a Excel para análisis
3. Crea órdenes de compra con múltiples productos
4. Revisa movimientos de stock para auditoría
5. Usa filtros para encontrar productos con bajo stock

### Para Gerentes
1. Revisa la auditoría regularmente
2. Cancela órdenes de compra si es necesario
3. Desactiva productos en lugar de eliminarlos
4. Exporta órdenes de compra para contabilidad
5. Monitorea el badge de stock bajo en el navbar

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### "No puedo ver la tienda"
→ Verifica que el servidor esté corriendo: `python manage.py runserver`

### "El carrito no se actualiza"
→ Revisa la consola del navegador (F12) para errores de JavaScript

### "No puedo agregar al carrito"
→ Verifica que el producto tenga stock disponible

### "No puedo acceder al dashboard"
→ Asegúrate de haber iniciado sesión con un usuario del sistema

### "El contador del carrito muestra 0"
→ Refresca la página, el contador se actualiza automáticamente

### "No veo el link a la tienda en el dashboard"
→ Verifica que estés autenticado

---

## 📞 CONTACTO Y SOPORTE

Para problemas técnicos:
1. Revisa esta guía
2. Verifica logs de Django en la consola
3. Revisa consola del navegador (F12)
4. Verifica que todas las migraciones estén aplicadas

---

**Última Actualización:** 25 de Abril, 2026
**Versión del Sistema:** 1.0
