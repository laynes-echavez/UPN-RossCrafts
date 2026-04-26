# 🧪 GUÍA DE TESTING VISUAL - HOMEPAGE ACTUALIZADA

## 🎯 OBJETIVO

Verificar que la homepage actualizada con Tailwind CSS se muestra correctamente y todas las funcionalidades operan como se espera.

---

## 🚀 PASO 1: INICIAR EL SERVIDOR

### Opción A: Desde la terminal

```bash
python manage.py runserver
```

### Opción B: Desde VS Code
1. Abrir terminal integrada (Ctrl + `)
2. Ejecutar: `python manage.py runserver`

**Resultado esperado:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🌐 PASO 2: ABRIR LA HOMEPAGE

1. Abrir navegador (Chrome, Firefox, Edge)
2. Ir a: `http://127.0.0.1:8000/`

---

## ✅ PASO 3: VERIFICACIÓN VISUAL

### 3.1 Navbar (Barra de Navegación Superior)

**Debe verse así:**
- ✅ Fondo verde oscuro (#41431B)
- ✅ Logo "Ross Crafts" con icono de paleta a la izquierda
- ✅ Links: "Inicio", "Tienda"
- ✅ Link "Iniciar Sesión" (si no estás autenticado)
- ✅ Link "Carrito" con badge rojo mostrando "0"
- ✅ Navbar se queda fijo al hacer scroll (sticky)

**Probar:**
1. Hacer scroll hacia abajo → Navbar debe quedarse fijo arriba
2. Hover sobre los links → Deben cambiar de color (efecto hover)
3. Click en "Inicio" → Debe recargar la página
4. Click en "Tienda" → Debe ir al catálogo

### 3.2 Hero Section (Sección Principal)

**Debe verse así:**
- ✅ Fondo con gradiente verde (oscuro → medio)
- ✅ Patrón decorativo sutil en el fondo
- ✅ Título grande: "Descubre el Mundo de las Manualidades"
- ✅ Subtítulo: "Productos artesanales únicos..."
- ✅ Barra de búsqueda blanca con placeholder
- ✅ Botón "Buscar" blanco con texto verde
- ✅ Botón "Ver Tienda" blanco con sombra

**Probar:**
1. Escribir algo en la búsqueda → Debe permitir escribir
2. Click en "Buscar" → Debe ir al catálogo con búsqueda
3. Click en "Ver Tienda" → Debe ir al catálogo
4. Hover sobre botones → Deben tener efecto de elevación

### 3.3 Categorías Destacadas

**Debe verse así:**
- ✅ Título: "Explora por Categorías"
- ✅ Subtítulo: "Encuentra exactamente lo que necesitas"
- ✅ Grid de 3 columnas (en desktop)
- ✅ Cards beige (#E3DBBB) con iconos grandes
- ✅ Nombre de categoría y contador de productos

**Probar:**
1. Hover sobre una card → Debe elevarse y cambiar a verde medio
2. Hover sobre icono → Debe cambiar a blanco
3. Click en una categoría → Debe ir al catálogo filtrado

**Categorías esperadas:**
- Textiles (icono: camiseta)
- Cerámica (icono: taza)
- Joyería (icono: gema)
- Decoración (icono: casa)
- Otras (icono: paleta)

### 3.4 Productos Destacados

**Debe verse así:**
- ✅ Título: "Productos Destacados"
- ✅ Subtítulo: "Lo más nuevo de nuestra colección"
- ✅ Grid de 4 columnas (en desktop)
- ✅ Cards blancas con sombra
- ✅ Imagen del producto (o gradiente si no hay imagen)
- ✅ Nombre del producto (máximo 2 líneas)
- ✅ Precio en grande: "S/. XX.XX"
- ✅ Badge verde "Disponible" o rojo "Agotado"
- ✅ Botón "Agregar al Carrito" verde

**Probar:**
1. Hover sobre una card → Debe elevarse
2. Hover sobre imagen → Debe hacer zoom
3. Click en imagen → Debe ir al detalle del producto
4. Click en nombre → Debe ir al detalle del producto
5. Click en "Agregar al Carrito" → Debe:
   - Mostrar notificación verde "Producto agregado al carrito"
   - Actualizar el badge del carrito en el navbar
   - La notificación debe desaparecer después de 3 segundos

### 3.5 Características

**Debe verse así:**
- ✅ Grid de 3 columnas
- ✅ Iconos grandes en círculos con fondo verde claro
- ✅ Títulos: "Envío a Todo el Perú", "Hecho a Mano", "Compra Segura"
- ✅ Descripciones debajo de cada título

**Iconos esperados:**
- Envío: camión (fa-shipping-fast)
- Hecho a Mano: corazón en mano (fa-hand-holding-heart)
- Compra Segura: escudo (fa-shield-alt)

### 3.6 Footer (Pie de Página)

**Debe verse así:**
- ✅ Fondo verde oscuro (#41431B)
- ✅ Texto blanco
- ✅ Grid de 3 columnas:
  1. Logo y descripción
  2. Enlaces (Tienda, Políticas, Términos)
  3. Contacto e iconos sociales
- ✅ Línea separadora
- ✅ Copyright centrado: "© 2026 Ross Crafts..."

**Probar:**
1. Hover sobre links → Deben cambiar a blanco puro
2. Hover sobre iconos sociales → Deben cambiar a verde medio
3. Click en "Tienda" → Debe ir al catálogo

---

## 📱 PASO 4: VERIFICACIÓN RESPONSIVE

### 4.1 Desktop (> 1024px)

**Abrir DevTools:**
- Windows/Linux: F12 o Ctrl + Shift + I
- Mac: Cmd + Option + I

**Verificar:**
- ✅ Navbar completo con todos los links
- ✅ Categorías en 3 columnas
- ✅ Productos en 4 columnas
- ✅ Características en 3 columnas
- ✅ Footer en 3 columnas

### 4.2 Tablet (768px - 1024px)

**En DevTools:**
1. Click en icono de dispositivo móvil (Toggle device toolbar)
2. Seleccionar "iPad" o establecer ancho a 768px

**Verificar:**
- ✅ Navbar completo
- ✅ Categorías en 2 columnas
- ✅ Productos en 2 columnas
- ✅ Características en 3 columnas
- ✅ Footer en 3 columnas

### 4.3 Mobile (< 768px)

**En DevTools:**
1. Seleccionar "iPhone 12" o establecer ancho a 375px

**Verificar:**
- ✅ Menú hamburguesa (3 líneas) visible
- ✅ Logo visible
- ✅ Badge del carrito visible
- ✅ Categorías en 1 columna
- ✅ Productos en 1 columna
- ✅ Características en 1 columna
- ✅ Footer en 1 columna

**Probar menú móvil:**
1. Click en icono hamburguesa → Debe abrir menú
2. Menú debe mostrar:
   - Inicio
   - Tienda
   - Iniciar Sesión (o Dashboard si estás autenticado)
   - Carrito (0)
3. Click en cualquier link → Debe funcionar
4. Click en hamburguesa de nuevo → Debe cerrar menú

---

## 🛒 PASO 5: VERIFICACIÓN DE FUNCIONALIDAD DEL CARRITO

### 5.1 Agregar Producto al Carrito

1. Scroll hasta "Productos Destacados"
2. Click en "Agregar al Carrito" en cualquier producto

**Resultado esperado:**
- ✅ Aparece notificación verde: "Producto agregado al carrito"
- ✅ Badge del carrito cambia de "0" a "1"
- ✅ Notificación desaparece después de 3 segundos

### 5.2 Agregar Múltiples Productos

1. Click en "Agregar al Carrito" en otro producto
2. Click en "Agregar al Carrito" en otro producto más

**Resultado esperado:**
- ✅ Badge del carrito se actualiza a "2", luego "3"
- ✅ Cada vez aparece la notificación

### 5.3 Ver Carrito

1. Click en "Carrito" en el navbar

**Resultado esperado:**
- ✅ Redirige a `/carrito/`
- ✅ Muestra los productos agregados
- ✅ Muestra cantidades y precios

---

## 🔍 PASO 6: VERIFICACIÓN DE BÚSQUEDA

### 6.1 Búsqueda desde Hero

1. En la barra de búsqueda del hero, escribir: "collar"
2. Click en "Buscar"

**Resultado esperado:**
- ✅ Redirige a `/tienda/?search=collar`
- ✅ Muestra productos que coinciden con "collar"

### 6.2 Búsqueda Vacía

1. Dejar la búsqueda vacía
2. Click en "Buscar"

**Resultado esperado:**
- ✅ Redirige a `/tienda/`
- ✅ Muestra todos los productos

---

## 🎨 PASO 7: VERIFICACIÓN DE COLORES

### Paleta de Colores de Ross Crafts

Verificar que estos colores se usen consistentemente:

| Color | Código | Uso |
|-------|--------|-----|
| Verde Oscuro | #41431B | Navbar, botones principales |
| Verde Medio | #AEB784 | Hover effects, categorías |
| Beige | #E3DBBB | Cards de categorías |
| Crema | #F8F3E1 | Fondo de secciones |

**Verificar en DevTools:**
1. Click derecho en un elemento → Inspeccionar
2. En la pestaña "Computed", buscar "background-color"
3. Verificar que coincida con los colores de la paleta

---

## 🐛 PASO 8: VERIFICACIÓN DE ERRORES

### 8.1 Consola de JavaScript

**En DevTools → Console:**
- ✅ No debe haber errores en rojo
- ⚠️ Puede haber warnings en amarillo (normal)

**Errores comunes a buscar:**
- ❌ "Failed to load resource" → Verificar que Tailwind CDN esté cargando
- ❌ "Uncaught ReferenceError" → Verificar que funciones JS estén definidas
- ❌ "CSRF token missing" → Verificar que csrftoken esté definido

### 8.2 Network (Red)

**En DevTools → Network:**
1. Recargar la página (F5)
2. Verificar que todos los recursos carguen con status 200

**Recursos esperados:**
- ✅ `tailwindcss.com` → Status 200
- ✅ `cdnjs.cloudflare.com/ajax/libs/font-awesome` → Status 200
- ✅ `fonts.googleapis.com` → Status 200

### 8.3 Terminal del Servidor

**En la terminal donde corre el servidor:**
- ✅ No debe haber errores en rojo
- ✅ Debe mostrar requests GET con status 200

**Ejemplo de output esperado:**
```
[26/Apr/2026 10:30:15] "GET / HTTP/1.1" 200 15234
[26/Apr/2026 10:30:16] "GET /carrito/contador/ HTTP/1.1" 200 25
```

---

## ✅ CHECKLIST FINAL

### Visual
- [ ] Navbar se muestra correctamente
- [ ] Hero section con gradiente
- [ ] Categorías en grid
- [ ] Productos en grid
- [ ] Características en grid
- [ ] Footer se muestra correctamente

### Funcionalidad
- [ ] Links del navbar funcionan
- [ ] Búsqueda funciona
- [ ] Agregar al carrito funciona
- [ ] Notificación toast aparece
- [ ] Badge del carrito se actualiza
- [ ] Links de categorías funcionan
- [ ] Links de productos funcionan

### Responsive
- [ ] Desktop (> 1024px) se ve bien
- [ ] Tablet (768-1024px) se ve bien
- [ ] Mobile (< 768px) se ve bien
- [ ] Menú hamburguesa funciona

### Performance
- [ ] Página carga rápido (< 2 segundos)
- [ ] No hay errores en Console
- [ ] Todos los recursos cargan (Network)
- [ ] Transiciones son suaves

---

## 🎉 RESULTADO ESPERADO

Si todo está correcto, deberías ver:

✅ **Homepage moderna y profesional**
- Diseño limpio con colores de Ross Crafts
- Totalmente responsive
- Transiciones suaves
- Funcionalidad completa del carrito

✅ **Sin errores**
- Console limpia
- Network sin errores 404
- Terminal sin errores

✅ **Performance óptima**
- Carga rápida
- Interacciones fluidas
- Animaciones suaves

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema 1: Estilos no se aplican

**Síntomas:**
- Página se ve sin estilos
- Todo es texto plano
- No hay colores

**Solución:**
1. Verificar que Tailwind CDN esté cargando:
   - DevTools → Network → buscar "tailwindcss"
   - Debe aparecer con status 200
2. Si no carga, verificar conexión a internet
3. Limpiar caché del navegador (Ctrl + Shift + R)

### Problema 2: Contador del carrito no se actualiza

**Síntomas:**
- Badge siempre muestra "0"
- No cambia al agregar productos

**Solución:**
1. Verificar en Console si hay errores
2. Verificar que `/carrito/contador/` responda:
   - Ir a `http://127.0.0.1:8000/carrito/contador/`
   - Debe mostrar: `{"cart_count": 0}`
3. Verificar que función `updateCartCount()` esté definida

### Problema 3: Notificación no aparece

**Síntomas:**
- Al agregar al carrito no aparece notificación
- No hay feedback visual

**Solución:**
1. Verificar en Console si hay errores
2. Verificar que función `addToCart()` esté definida
3. Verificar que CSRF token esté definido

### Problema 4: Menú móvil no funciona

**Síntomas:**
- Click en hamburguesa no hace nada
- Menú no se abre

**Solución:**
1. Verificar en Console si hay errores
2. Verificar que función `toggleMobileMenu()` esté definida
3. Verificar que elemento `#mobile-menu` exista

### Problema 5: Imágenes no se muestran

**Síntomas:**
- Productos sin imagen
- Solo se ven gradientes

**Solución:**
1. Verificar que productos tengan imágenes en la base de datos
2. Verificar configuración de MEDIA_URL y MEDIA_ROOT
3. Verificar que archivos de imagen existan en media/

---

## 📞 CONTACTO

Si después de seguir esta guía encuentras problemas:

1. **Revisar documentación:**
   - `RESUMEN_ACTUALIZACION_TAILWIND.md`
   - `TAILWIND_HOMEPAGE_ACTUALIZADA.md`
   - `TAILWIND_GUIA_COMPLETA.md`

2. **Verificar archivos:**
   - `templates/store/base_store.html`
   - `templates/store/home.html`
   - `apps/ecommerce/views.py`

3. **Ejecutar tests:**
   ```bash
   python test_templates.py
   python manage.py check
   ```

---

**Fecha:** 26 de Abril, 2026  
**Versión:** 1.0  
**Estado:** ✅ Guía de Testing Completa
