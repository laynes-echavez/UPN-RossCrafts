# GUÍA DE USO - PUNTO DE VENTA (POS)

## Acceso al Sistema

### 1. Iniciar Sesión
- URL: `http://localhost:8000/auth/login/`
- Usuarios con acceso al POS:
  - **Empleado**: `empleado` / `Ross2026!`
  - **Administrador**: `admin` / `Ross2026!`

### 2. Acceder al POS
- Después de iniciar sesión, ir a: `http://localhost:8000/dashboard/pos/`
- O usar el menú de navegación

---

## Interfaz del POS

### Columna Izquierda - Catálogo de Productos
```
┌─────────────────────────────────────┐
│  🔍 Buscar productos...             │
├─────────────────────────────────────┤
│  ┌─────┐  ┌─────┐  ┌─────┐         │
│  │ P1  │  │ P2  │  │ P3  │         │
│  │$100 │  │$200 │  │$150 │         │
│  └─────┘  └─────┘  └─────┘         │
│  ┌─────┐  ┌─────┐  ┌─────┐         │
│  │ P4  │  │ P5  │  │ P6  │         │
│  └─────┘  └─────┘  └─────┘         │
└─────────────────────────────────────┘
```

### Columna Derecha - Carrito
```
┌─────────────────────────────────────┐
│  🛒 Carrito de Compra               │
├─────────────────────────────────────┤
│  Producto 1    [-] 2 [+]  S/. 200  │
│  Producto 2    [-] 1 [+]  S/. 150  │
├─────────────────────────────────────┤
│  👤 Cliente (Opcional)              │
│  🔍 Buscar cliente...               │
├─────────────────────────────────────┤
│  💰 Descuento                       │
│  [  5.00  ] [Monto ▼]              │
├─────────────────────────────────────┤
│  💳 Método de Pago                  │
│  [Efectivo] [Tarjeta] [Transfer.]  │
├─────────────────────────────────────┤
│  Subtotal:      S/. 350.00          │
│  Descuento:   - S/.   5.00          │
│  IGV (18%):     S/.  62.10          │
│  ─────────────────────────           │
│  TOTAL:         S/. 407.10          │
├─────────────────────────────────────┤
│  [    REGISTRAR VENTA    ]          │
└─────────────────────────────────────┘
```

---

## Flujo de Trabajo

### Paso 1: Buscar Productos
1. Escribir en el buscador (mínimo 2 caracteres)
2. Busca por nombre o SKU
3. Aparecen productos en tiempo real

### Paso 2: Agregar al Carrito
1. Click en la card del producto
2. Se agrega automáticamente con cantidad 1
3. Si ya está en el carrito, aumenta la cantidad

### Paso 3: Ajustar Cantidades
- **Botón [-]**: Disminuir cantidad (mínimo 1)
- **Input numérico**: Escribir cantidad directa
- **Botón [+]**: Aumentar cantidad (máximo = stock disponible)
- **Botón [×]**: Eliminar producto del carrito

### Paso 4: Seleccionar Cliente (Opcional)
#### Opción A: Buscar Cliente Existente
1. Escribir en "Buscar cliente..."
2. Busca por: nombre, apellido, email o DNI
3. Click en el cliente deseado
4. Se muestra el nombre seleccionado

#### Opción B: Registrar Nuevo Cliente
1. Click en "Nuevo Cliente"
2. Llenar formulario rápido:
   - Nombre ✓ (requerido)
   - Apellido ✓ (requerido)
   - DNI (8 dígitos)
   - Teléfono
   - Email
3. Click en "Guardar"
4. Cliente se selecciona automáticamente

### Paso 5: Aplicar Descuento (Opcional)
#### Descuento por Monto Fijo
1. Escribir cantidad en soles (ej: 5.00)
2. Seleccionar "Monto" en el dropdown
3. Se resta directamente del subtotal

#### Descuento por Porcentaje
1. Escribir porcentaje (ej: 10)
2. Seleccionar "%" en el dropdown
3. Se calcula sobre el subtotal

### Paso 6: Seleccionar Método de Pago
- Click en el método deseado:
  - 💵 **Efectivo** (por defecto)
  - 💳 **Tarjeta**
  - 🏦 **Transferencia**

### Paso 7: Registrar Venta
1. Verificar totales
2. Click en "REGISTRAR VENTA"
3. El sistema valida:
   - ✓ Carrito no vacío
   - ✓ Stock suficiente
4. Procesamiento:
   - Crea la venta
   - Descuenta del stock
   - Genera comprobante

### Paso 8: Confirmación
Modal muestra:
- ✅ Venta registrada
- Número de comprobante: RC-2026-XXXXXX
- Total cobrado

Opciones:
- **🖨️ Imprimir**: Abre PDF del comprobante
- **Nueva Venta**: Limpia el carrito

---

## Cálculo de Totales

### Fórmulas
```
1. Subtotal = Σ(precio × cantidad)

2. Descuento:
   - Monto fijo: descuento
   - Porcentaje: subtotal × (porcentaje / 100)

3. Base imponible = Subtotal - Descuento

4. IGV (18%) = Base imponible × 0.18

5. TOTAL = Base imponible + IGV
```

### Ejemplo
```
Producto A: S/. 100 × 2 = S/. 200
Producto B: S/. 150 × 1 = S/. 150
─────────────────────────────────
Subtotal:              S/. 350.00
Descuento (fijo):    - S/.   5.00
─────────────────────────────────
Base imponible:        S/. 345.00
IGV (18%):             S/.  62.10
─────────────────────────────────
TOTAL:                 S/. 407.10
```

---

## Comprobante de Venta

### Formato del Número
```
RC-YYYY-XXXXXX

RC     = Ross Crafts
YYYY   = Año actual
XXXXXX = Número correlativo (6 dígitos)

Ejemplo: RC-2026-000001
```

### Contenido del PDF
```
╔════════════════════════════════════╗
║   COMPROBANTE DE VENTA             ║
║   Ross Crafts                      ║
╠════════════════════════════════════╣
║ Comprobante: RC-2026-000001        ║
║ Fecha: 26/04/2026 14:30           ║
║ Atendido por: Juan Pérez          ║
║ Cliente: María García             ║
║ DNI: 12345678                     ║
╠════════════════════════════════════╣
║ Descripción    Cant  P.Unit  Sub  ║
║ Producto A       2   100.00  200  ║
║ Producto B       1   150.00  150  ║
╠════════════════════════════════════╣
║ Subtotal:              S/. 350.00 ║
║ Descuento:           - S/.   5.00 ║
║ IGV (18%):             S/.  62.10 ║
║ ─────────────────────────────────  ║
║ TOTAL:                 S/. 407.10 ║
╠════════════════════════════════════╣
║ Método de pago: Efectivo          ║
╠════════════════════════════════════╣
║ Gracias por su compra             ║
║ Ross Crafts                       ║
╚════════════════════════════════════╝
```

---

## Indicadores Visuales

### Badges de Stock
- 🔴 **Stock Bajo**: ≤ 5 unidades (badge rojo)
- ✅ **Stock OK**: > 5 unidades (sin badge)
- ⚫ **Sin Stock**: 0 unidades (card deshabilitada)

### Colores del Sistema
- **#41431B** (Verde oscuro): Headers, botones principales
- **#AEB784** (Verde medio): Botones secundarios
- **#E3DBBB** (Beige claro): Fondo del carrito
- **#F8F3E1** (Crema): Fondo de la página

### Estados del Carrito
- **Vacío**: Mensaje "El carrito está vacío"
- **Con productos**: Lista de items con controles
- **Botón deshabilitado**: Cuando el carrito está vacío

---

## Validaciones y Errores

### Validaciones Automáticas
✓ Stock disponible al agregar producto
✓ Cantidad máxima = stock disponible
✓ Cantidad mínima = 1
✓ Carrito no vacío al registrar venta
✓ Stock suficiente al confirmar venta

### Mensajes de Error Comunes

#### "Stock insuficiente para [Producto]"
- **Causa**: Otro usuario vendió el producto mientras estabas en el POS
- **Solución**: Ajustar cantidad o eliminar del carrito

#### "El carrito está vacío"
- **Causa**: Intentar registrar venta sin productos
- **Solución**: Agregar productos al carrito

#### "No hay suficiente stock disponible"
- **Causa**: Intentar agregar más unidades de las disponibles
- **Solución**: Verificar stock actual del producto

---

## Atajos de Teclado

### En el Buscador de Productos
- **Enter**: Buscar
- **Esc**: Limpiar búsqueda

### En el Input de Cantidad
- **↑**: Aumentar cantidad
- **↓**: Disminuir cantidad
- **Enter**: Confirmar cantidad

---

## Consejos y Mejores Prácticas

### 1. Búsqueda Eficiente
- Usar SKU para búsqueda rápida
- Escribir al menos 2 caracteres
- Esperar resultados en tiempo real

### 2. Gestión del Carrito
- Verificar cantidades antes de registrar
- Usar botones +/- para ajustes rápidos
- Eliminar productos no deseados

### 3. Clientes
- Registrar cliente para historial de compras
- Usar búsqueda por DNI para rapidez
- Registro rápido solo con datos esenciales

### 4. Descuentos
- Aplicar descuentos autorizados
- Verificar cálculo antes de confirmar
- Usar porcentaje para promociones

### 5. Comprobantes
- Imprimir inmediatamente después de venta
- Verificar datos del cliente
- Guardar PDF si es necesario

---

## Solución de Problemas

### Problema: No aparecen productos
**Solución**:
1. Verificar que hay productos activos
2. Verificar que tienen stock > 0
3. Escribir al menos 2 caracteres en búsqueda

### Problema: No se puede agregar al carrito
**Solución**:
1. Verificar stock disponible
2. Verificar que el producto está activo
3. Refrescar la página

### Problema: Error al registrar venta
**Solución**:
1. Verificar conexión a internet
2. Verificar que hay stock suficiente
3. Verificar que el carrito no está vacío
4. Contactar al administrador

### Problema: No se genera el PDF
**Solución**:
1. Verificar que el navegador permite pop-ups
2. Verificar que ReportLab está instalado
3. Intentar descargar desde el historial de ventas

---

## Soporte Técnico

### Contacto
- **Administrador del Sistema**: admin@rosscrafts.com
- **Soporte Técnico**: soporte@rosscrafts.com

### Información del Sistema
- **Versión**: 1.0.0
- **Framework**: Django 4.2+
- **Base de datos**: SQL Server Express
- **Navegadores soportados**: Chrome, Firefox, Edge

---

## Historial de Cambios

### Versión 1.0.0 (26/04/2026)
- ✅ Implementación inicial del POS
- ✅ Búsqueda de productos en tiempo real
- ✅ Gestión de carrito
- ✅ Búsqueda y registro de clientes
- ✅ Aplicación de descuentos
- ✅ Múltiples métodos de pago
- ✅ Generación de comprobantes PDF
- ✅ Actualización automática de stock

---

**Última actualización**: 26 de Abril, 2026
