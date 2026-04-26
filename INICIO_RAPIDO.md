# 🚀 INICIO RÁPIDO - ROSS CRAFTS

## ⚡ Guía de 5 Minutos

### 1️⃣ Iniciar el Servidor
```bash
# Activar entorno virtual
venv\Scripts\activate

# Iniciar servidor
python manage.py runserver
```

### 2️⃣ Acceder a la Tienda Online
Abre tu navegador en: **http://127.0.0.1:8000/**

**Lo que verás:**
- 🏠 Página de inicio con hero banner
- 🎨 Categorías destacadas
- ⭐ Productos destacados
- 🛒 Carrito de compras

**Prueba esto:**
1. Haz clic en "Ver Tienda"
2. Explora el catálogo
3. Haz clic en un producto
4. Agrega al carrito
5. Ve al carrito (ícono 🛒 arriba)

---

### 3️⃣ Acceder al Dashboard
Abre en otra pestaña: **http://127.0.0.1:8000/auth/login/**

**Usuarios de Prueba:**

| Usuario | Contraseña | Rol | Acceso |
|---------|-----------|-----|--------|
| gerente | Ross2026! | Gerente | Todo |
| admin | Ross2026! | Administrador | Gestión + POS |
| empleado | Ross2026! | Empleado | POS + Clientes |

**Prueba esto:**
1. Inicia sesión con "admin" / "Ross2026!"
2. Serás redirigido al POS
3. Busca un producto
4. Agrega al carrito
5. Registra una venta

---

## 🗺️ MAPA RÁPIDO DEL SISTEMA

### 🏪 TIENDA ONLINE (Para Clientes)
```
http://127.0.0.1:8000/
├── /                    → Inicio
├── /tienda/             → Catálogo
├── /tienda/<slug>/      → Detalle de producto
└── /carrito/            → Carrito de compras
```

### 💼 DASHBOARD (Para Empleados)
```
http://127.0.0.1:8000/auth/login/
├── /pos/                → Punto de Venta
├── /stock/              → Productos
├── /clientes/           → Clientes
├── /proveedores/        → Proveedores
├── /compras/            → Órdenes de Compra
├── /reports/            → Reportes (Gerente)
└── /dashboard/auditoria/ → Auditoría (Gerente)
```

---

## 🎯 FLUJOS PRINCIPALES

### Flujo 1: Cliente Comprando
```
1. Entra a la tienda (/)
2. Busca o explora productos
3. Hace clic en un producto
4. Agrega al carrito
5. Ve al carrito
6. Revisa productos
7. [Checkout pendiente]
```

### Flujo 2: Empleado Vendiendo
```
1. Login como empleado
2. Redirige al POS
3. Busca productos
4. Agrega al carrito
5. Busca/registra cliente
6. Aplica descuento (opcional)
7. Registra venta
8. Imprime recibo
```

### Flujo 3: Admin Gestionando Productos
```
1. Login como admin
2. Va a Productos (/stock/)
3. Crea nuevo producto
4. Define precio, stock, categoría
5. Sube imagen (opcional)
6. Guarda
7. Producto aparece en tienda
```

### Flujo 4: Gerente Recibiendo Orden
```
1. Login como gerente
2. Va a Órdenes de Compra (/compras/)
3. Crea nueva orden
4. Selecciona proveedor
5. Agrega productos
6. Guarda (estado: Pendiente)
7. Cuando llega, marca como Recibida
8. Stock se actualiza automáticamente
```

---

## 🔑 FUNCIONALIDADES CLAVE

### ✅ Ya Implementadas

#### Tienda Online
- ✅ Catálogo con filtros
- ✅ Búsqueda de productos
- ✅ Carrito de compras
- ✅ Persistencia de carrito
- ✅ Diseño responsive

#### Dashboard
- ✅ Gestión de productos
- ✅ Gestión de clientes
- ✅ Gestión de proveedores
- ✅ Órdenes de compra
- ✅ Punto de venta (POS)
- ✅ Reportes
- ✅ Auditoría

#### Seguridad
- ✅ Autenticación por roles
- ✅ Rate limiting en login
- ✅ CSRF protection
- ✅ Auditoría de acciones

### ⏳ Pendientes

- ⏳ Checkout y pagos
- ⏳ Registro de clientes desde tienda
- ⏳ Notificaciones por email
- ⏳ Tracking de pedidos

---

## 🎨 CARACTERÍSTICAS DE DISEÑO

### Paleta de Colores
- **Verde Oscuro (#41431B):** Navbar, botones
- **Verde Medio (#AEB784):** Hover, acentos
- **Beige Claro (#E3DBBB):** Fondos, bordes
- **Crema (#F8F3E1):** Fondo general

### Responsive
- **Desktop:** 3 columnas de productos
- **Tablet:** 2 columnas
- **Mobile:** 1 columna

---

## 🐛 SOLUCIÓN RÁPIDA DE PROBLEMAS

### El servidor no inicia
```bash
# Verifica que el entorno virtual esté activo
venv\Scripts\activate

# Verifica las migraciones
python manage.py migrate
```

### No veo productos en la tienda
```bash
# Pobla datos de prueba
python populate_test_data.py
python populate_product_slugs.py
```

### Error al agregar al carrito
- Abre la consola del navegador (F12)
- Verifica errores de JavaScript
- Refresca la página (Ctrl+F5)

### No puedo iniciar sesión
- Usuario: **admin**
- Contraseña: **Ross2026!**
- Verifica que las mayúsculas estén correctas

---

## 📚 DOCUMENTACIÓN COMPLETA

Para más detalles, consulta:

1. **RESUMEN_PROYECTO_COMPLETO.md** - Visión general
2. **GUIA_NAVEGACION_COMPLETA.md** - Mapa detallado
3. **ECOMMERCE_COMPLETADO.md** - Tienda online
4. **GUIA_USO_POS.md** - Punto de venta
5. **TEST_ECOMMERCE.md** - Checklist de testing

---

## 🎓 TIPS RÁPIDOS

### Para Clientes
💡 El carrito persiste mientras navegas  
💡 Puedes filtrar por categoría y precio  
💡 Inicia sesión para guardar tu carrito  

### Para Empleados
💡 El POS es tu pantalla principal  
💡 Usa Enter para buscar productos rápido  
💡 Puedes registrar clientes sin salir del POS  

### Para Administradores
💡 Importa productos desde Excel  
💡 Exporta clientes para análisis  
💡 El stock se actualiza automáticamente  

### Para Gerentes
💡 Revisa la auditoría regularmente  
💡 Monitorea el badge de stock bajo  
💡 Exporta órdenes para contabilidad  

---

## 🚀 COMANDOS ÚTILES

```bash
# Iniciar servidor
python manage.py runserver

# Verificar sistema
python manage.py check

# Crear superusuario
python manage.py createsuperuser

# Poblar datos de prueba
python populate_test_data.py

# Shell de Django
python manage.py shell

# Ver migraciones
python manage.py showmigrations
```

---

## 📞 ¿NECESITAS AYUDA?

1. Revisa la documentación en los archivos .md
2. Verifica los logs en la consola
3. Abre DevTools del navegador (F12)
4. Verifica que las migraciones estén aplicadas

---

## ✅ CHECKLIST DE INICIO

- [ ] Entorno virtual activado
- [ ] Servidor corriendo
- [ ] Tienda accesible en http://127.0.0.1:8000/
- [ ] Dashboard accesible en http://127.0.0.1:8000/auth/login/
- [ ] Puedes iniciar sesión con admin/Ross2026!
- [ ] Ves productos en la tienda
- [ ] Puedes agregar al carrito
- [ ] El POS funciona

---

**¡Listo! Ya puedes empezar a usar Ross Crafts** 🎉

**Próximo paso:** Explora la tienda y el dashboard para familiarizarte con todas las funcionalidades.

---

**Versión:** 1.0  
**Fecha:** 25 de Abril, 2026  
**Estado:** ✅ FUNCIONAL
