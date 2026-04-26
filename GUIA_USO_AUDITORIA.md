# 📋 GUÍA DE USO - SISTEMA DE AUDITORÍA

## 🎯 Descripción General

El sistema de auditoría de Ross Crafts registra automáticamente todas las acciones realizadas por usuarios del staff en áreas administrativas del sistema. Esto permite:

- Rastrear quién hizo qué y cuándo
- Detectar accesos no autorizados
- Cumplir con requisitos de auditoría
- Investigar incidentes de seguridad
- Monitorear el uso del sistema

---

## 🔐 Acceso al Sistema de Auditoría

### Requisitos
- Usuario autenticado con rol de **Gerente**
- Solo los gerentes pueden ver los registros de auditoría

### URL de Acceso
```
http://localhost:8000/dashboard/auditoria/
```

### Desde el Menú
1. Iniciar sesión como gerente
2. En el menú superior, hacer clic en **"Auditoría"** (icono de escudo)

---

## 📊 Vista Principal de Auditoría

### Información Mostrada

La tabla de auditoría muestra:

| Columna | Descripción |
|---------|-------------|
| **Fecha/Hora** | Momento exacto de la acción |
| **Usuario** | Nombre de usuario que realizó la acción |
| **Rol** | Rol del usuario (Gerente, Administrador, Empleado) |
| **Método** | Tipo de acción HTTP (GET, POST, DELETE, LOGIN, LOGOUT) |
| **URL** | Ruta accedida (truncada a 60 caracteres) |
| **IP** | Dirección IP desde donde se realizó la acción |
| **Código HTTP** | Código de respuesta (200, 404, 500, etc.) |

### Códigos de Color

**Métodos HTTP:**
- 🔵 GET - Consulta de información
- 🟢 POST - Creación o modificación
- 🔴 DELETE - Eliminación
- 🟣 LOGIN - Inicio de sesión
- 🟡 LOGOUT - Cierre de sesión

**Códigos HTTP:**
- 🟢 200-299 - Éxito
- 🔵 300-399 - Redirección
- 🟡 400-499 - Error del cliente
- 🔴 500-599 - Error del servidor

---

## 🔍 Filtros Disponibles

### 1. Filtro por Usuario
- Dropdown con todos los usuarios del staff
- Muestra: nombre de usuario y rol
- Seleccionar "Todos los usuarios" para ver todos

**Ejemplo de uso:**
```
Quiero ver solo las acciones de "juan_admin"
→ Seleccionar "juan_admin (Administrador)" en el dropdown
```

### 2. Filtro por Método
- GET - Ver consultas de información
- POST - Ver creaciones y modificaciones
- PUT - Ver actualizaciones
- DELETE - Ver eliminaciones
- LOGIN - Ver inicios de sesión
- LOGOUT - Ver cierres de sesión

**Ejemplo de uso:**
```
Quiero ver todos los intentos de login
→ Seleccionar "LOGIN" en el dropdown de método
```

### 3. Filtro por Rango de Fechas

**Desde (date_from):**
- Fecha inicial del rango
- Incluye todas las acciones desde las 00:00:00 de ese día

**Hasta (date_to):**
- Fecha final del rango
- Incluye todas las acciones hasta las 23:59:59 de ese día

**Ejemplo de uso:**
```
Quiero ver las acciones de la semana pasada
→ Desde: 2026-04-18
→ Hasta: 2026-04-24
```

### Aplicar Filtros
1. Seleccionar los filtros deseados
2. Hacer clic en el botón **🔍** (filtro)
3. La tabla se actualizará con los resultados

### Limpiar Filtros
- Hacer clic en "Auditoría" en el menú
- O acceder directamente a `/dashboard/auditoria/`

---

## 📄 Paginación

- **25 registros por página**
- Máximo **500 registros** mostrados (los más recientes)
- Navegación:
  - **Primera** - Ir a la primera página
  - **Anterior** - Página anterior
  - **Siguiente** - Página siguiente
  - **Última** - Ir a la última página

---

## 📥 Exportación a Excel

### Características
- Exporta los registros con los **filtros aplicados**
- Formato: `.xlsx` (Excel)
- Nombre: `auditoria_YYYYMMDD_HHMMSS.xlsx`
- Límite: 500 registros más recientes

### Cómo Exportar
1. Aplicar los filtros deseados (opcional)
2. Hacer clic en **"Exportar a Excel"** (botón verde)
3. El archivo se descargará automáticamente

### Contenido del Excel
- Encabezados con estilo profesional (fondo oscuro, texto blanco)
- Columnas ajustadas automáticamente
- Datos formateados:
  - Fecha/Hora: `YYYY-MM-DD HH:MM:SS`
  - Usuario y Rol
  - Método HTTP
  - URL completa
  - Dirección IP
  - Código HTTP

---

## 🔎 Casos de Uso Comunes

### 1. Investigar Actividad Sospechosa

**Escenario:** Se detectó un cambio no autorizado en el inventario

**Pasos:**
1. Ir a Auditoría
2. Filtrar por URL: buscar registros con `/stock/`
3. Filtrar por fecha: día del incidente
4. Revisar quién accedió y qué hizo
5. Exportar a Excel para documentación

### 2. Auditar Inicios de Sesión

**Escenario:** Verificar intentos de acceso al sistema

**Pasos:**
1. Ir a Auditoría
2. Filtrar por Método: `LOGIN`
3. Revisar códigos HTTP:
   - 200 = Login exitoso
   - 401 = Login fallido
4. Identificar IPs sospechosas

### 3. Monitorear Actividad de un Usuario

**Escenario:** Revisar qué ha hecho un empleado específico

**Pasos:**
1. Ir a Auditoría
2. Filtrar por Usuario: seleccionar el empleado
3. Filtrar por fecha: período deseado
4. Revisar todas sus acciones
5. Exportar para reporte

### 4. Detectar Accesos Fuera de Horario

**Escenario:** Verificar accesos en horarios no laborales

**Pasos:**
1. Ir a Auditoría
2. Filtrar por fecha: día específico
3. Revisar columna Fecha/Hora
4. Identificar accesos fuera de horario (ej: 2:00 AM)
5. Verificar IP y usuario

### 5. Auditar Eliminaciones

**Escenario:** Rastrear qué se ha eliminado del sistema

**Pasos:**
1. Ir a Auditoría
2. Filtrar por Método: `DELETE`
3. Revisar URLs para identificar qué se eliminó
4. Verificar usuario responsable
5. Exportar para documentación

---

## 📊 Interpretación de Registros

### Ejemplo de Registro

```
Fecha/Hora: 2026-04-25 10:30:45
Usuario: juan_admin
Rol: Administrador
Método: POST
URL: /stock/products/15/edit/
IP: 192.168.1.100
Código HTTP: 200
```

**Interpretación:**
- El usuario `juan_admin` (Administrador)
- El 25 de abril de 2026 a las 10:30:45
- Realizó una modificación (POST)
- En el producto con ID 15
- Desde la IP 192.168.1.100
- La operación fue exitosa (200)

### Códigos HTTP Importantes

| Código | Significado | Acción |
|--------|-------------|--------|
| 200 | OK | Operación exitosa |
| 302 | Redirect | Redirección (normal) |
| 401 | Unauthorized | Login fallido |
| 403 | Forbidden | Acceso denegado |
| 404 | Not Found | Recurso no encontrado |
| 500 | Server Error | Error del servidor |

---

## 🚨 Alertas de Seguridad

### Situaciones que Requieren Atención

1. **Múltiples LOGIN con código 401**
   - Posible intento de acceso no autorizado
   - Verificar IP y usuario

2. **Accesos desde IPs desconocidas**
   - Verificar si es un acceso legítimo
   - Considerar bloquear la IP si es sospechosa

3. **Accesos fuera de horario laboral**
   - Verificar si el usuario tenía autorización
   - Revisar qué acciones realizó

4. **Múltiples DELETE en corto tiempo**
   - Posible eliminación masiva no autorizada
   - Verificar qué se eliminó

5. **Códigos 500 frecuentes**
   - Indica problemas técnicos
   - Revisar logs de errores

---

## 📝 Mejores Prácticas

### Para Gerentes

1. **Revisar auditoría regularmente**
   - Al menos una vez por semana
   - Después de incidentes reportados

2. **Exportar reportes mensuales**
   - Mantener archivo histórico
   - Útil para auditorías externas

3. **Investigar anomalías**
   - Accesos inusuales
   - Patrones sospechosos

4. **Documentar incidentes**
   - Exportar registros relevantes
   - Mantener evidencia

### Para el Sistema

1. **Limpieza periódica**
   - Los registros se acumulan
   - Considerar limpiar registros antiguos (>90 días)

2. **Monitoreo de espacio**
   - Verificar tamaño de la tabla `rc_audit_logs`
   - Implementar rotación si es necesario

3. **Backup de logs**
   - Incluir tabla de auditoría en backups
   - Mantener copias de seguridad

---

## 🔧 Solución de Problemas

### No veo el enlace de Auditoría
- **Causa:** No tienes rol de gerente
- **Solución:** Contactar al administrador del sistema

### No aparecen registros
- **Causa:** No se han realizado acciones auditables
- **Solución:** Los registros se crean automáticamente al usar el sistema

### Los filtros no funcionan
- **Causa:** Error en la consulta
- **Solución:** Limpiar filtros y volver a intentar

### No puedo exportar a Excel
- **Causa:** Problema con la librería openpyxl
- **Solución:** Verificar que openpyxl esté instalado

---

## 📞 Soporte

Si encuentras problemas con el sistema de auditoría:

1. Verificar que tienes rol de gerente
2. Revisar los logs del sistema en `logs/errors.log`
3. Contactar al administrador del sistema
4. Consultar la documentación técnica en `SEGURIDAD_AUDITORIA_COMPLETADO.md`

---

## 📚 Documentación Relacionada

- `SEGURIDAD_AUDITORIA_COMPLETADO.md` - Documentación técnica completa
- `test_security_audit.py` - Script de verificación del sistema
- `GUIA_USO_AUTENTICACION.md` - Guía de autenticación y roles

---

**Última actualización:** 25 de abril de 2026
