# 🚀 Guía de Despliegue en Producción - Ross Crafts

## 📋 Índice
1. [Requisitos del Servidor](#requisitos-del-servidor)
2. [Configuración de SQL Server](#configuración-de-sql-server)
3. [Configuración de la Aplicación](#configuración-de-la-aplicación)
4. [Despliegue con IIS](#despliegue-con-iis)
5. [Configuración SSL](#configuración-ssl)
6. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
7. [Solución de Problemas](#solución-de-problemas)

---

## 🖥️ Requisitos del Servidor

### Hardware Mínimo
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Disco:** 50 GB SSD
- **Red:** 100 Mbps

### Hardware Recomendado
- **CPU:** 4+ cores
- **RAM:** 8+ GB
- **Disco:** 100+ GB SSD
- **Red:** 1 Gbps

### Software Requerido
- Windows Server 2016+ o Windows 10/11 Pro
- SQL Server Express 2017+
- Python 3.12+
- ODBC Driver 17 for SQL Server
- IIS 10+
- Certificado SSL válido

---

## 🗄️ Configuración de SQL Server

### 1. Instalar SQL Server Express

Descargar desde: https://www.microsoft.com/sql-server/sql-server-downloads

Durante la instalación:
- Seleccionar "Modo de autenticación mixto" o "Solo Windows"
- Anotar el nombre de la instancia (ej: `SERVIDOR\SQLEXPRESS`)

### 2. Instalar ODBC Driver 17

```bash
# Descargar e instalar desde:
https://go.microsoft.com/fwlink/?linkid=2168524
```

### 3. Configurar Base de Datos

Ejecutar en SQL Server Management Studio (SSMS):

```sql
-- Abrir scripts\setup_production_db.sql
-- Modificar el usuario según tu configuración
-- Ejecutar el script completo
```

**Pasos del script:**
1. Crea la base de datos `ross_crafts_db`
2. Configura permisos para el usuario de IIS
3. Asigna roles necesarios (db_datareader, db_datawriter, db_ddladmin)
4. Verifica permisos

### 4. Verificar Conexión

```bash
python scripts\check_db.py
```

Debe mostrar:
```
✅ Conexión a SQL Server exitosa
   Versión: Microsoft SQL Server...
   Base de datos actual: ross_crafts_db
   Usuario del sistema: DOMINIO\usuario
```

---

## ⚙️ Configuración de la Aplicación

### 1. Clonar Repositorio

```bash
cd C:\inetpub\wwwroot
git clone https://github.com/tu-usuario/ross_crafts.git
cd ross_crafts
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Copiar y editar `.env`:

```bash
copy .env.example .env
notepad .env
```

**Configuración de Producción:**

```env
# Django
SECRET_KEY=genera-clave-secreta-muy-larga-y-aleatoria-aqui
DEBUG=False
ALLOWED_HOSTS=www.rosscrafts.com,rosscrafts.com,IP_DEL_SERVIDOR

# Base de datos
DB_NAME=ross_crafts_db
DB_HOST=SERVIDOR\SQLEXPRESS

# Stripe LIVE
STRIPE_PUBLIC_KEY=pk_live_tu_clave_real
STRIPE_SECRET_KEY=sk_live_tu_clave_real
STRIPE_WEBHOOK_SECRET=whsec_tu_clave_real

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=notificaciones@rosscrafts.com
EMAIL_HOST_PASSWORD=tu-password-de-aplicacion
DEFAULT_FROM_EMAIL=Ross Crafts <notificaciones@rosscrafts.com>

# Admin
ADMIN_EMAIL=admin@rosscrafts.com
```

**Generar SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Ejecutar Despliegue

```bash
deploy.bat
```

Este script:
1. Verifica conexión a BD
2. Instala dependencias
3. Aplica migraciones
4. Recolecta archivos estáticos
5. Carga datos iniciales
6. Verifica configuración

### 6. Crear Superusuario

```bash
python manage.py createsuperuser --settings=settings.production
```

---

## 🌐 Despliegue con IIS

### 1. Instalar IIS

**Windows Server:**
```powershell
Install-WindowsFeature -name Web-Server -IncludeManagementTools
```

**Windows 10/11:**
- Panel de Control > Programas > Activar o desactivar características de Windows
- Marcar "Internet Information Services"

### 2. Instalar wfastcgi

```bash
pip install wfastcgi
wfastcgi-enable
```

Anotar la ruta que devuelve (ej: `C:\...\wfastcgi.py`)

### 3. Crear Sitio Web en IIS

1. Abrir IIS Manager
2. Click derecho en "Sites" > "Add Website"
3. Configurar:
   - **Site name:** Ross Crafts
   - **Physical path:** `C:\inetpub\wwwroot\ross_crafts`
   - **Binding:** HTTP, Port 80, Hostname: www.rosscrafts.com
4. Click OK

### 4. Configurar FastCGI

Crear `web.config` en la raíz del proyecto:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="Python FastCGI" 
           path="*" 
           verb="*" 
           modules="FastCgiModule" 
           scriptProcessor="C:\inetpub\wwwroot\ross_crafts\venv\Scripts\python.exe|C:\inetpub\wwwroot\ross_crafts\venv\Lib\site-packages\wfastcgi.py" 
           resourceType="Unspecified" 
           requireAccess="Script" />
    </handlers>
    <staticContent>
      <mimeMap fileExtension=".woff" mimeType="application/font-woff" />
      <mimeMap fileExtension=".woff2" mimeType="application/font-woff2" />
    </staticContent>
  </system.webServer>
  <appSettings>
    <add key="WSGI_HANDLER" value="django.core.wsgi.get_wsgi_application()" />
    <add key="PYTHONPATH" value="C:\inetpub\wwwroot\ross_crafts" />
    <add key="DJANGO_SETTINGS_MODULE" value="settings.production" />
  </appSettings>
</configuration>
```

### 5. Configurar Permisos

```powershell
# Dar permisos al usuario de IIS
icacls "C:\inetpub\wwwroot\ross_crafts" /grant "IIS_IUSRS:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\ross_crafts\logs" /grant "IIS_IUSRS:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\ross_crafts\media" /grant "IIS_IUSRS:(OI)(CI)F" /T
```

### 6. Reiniciar IIS

```powershell
iisreset
```

---

## 🔒 Configuración SSL

### 1. Obtener Certificado SSL

**Opciones:**
- **Let's Encrypt:** Gratuito (win-acme para Windows)
- **Comprado:** GoDaddy, Namecheap, etc.

### 2. Instalar Certificado en IIS

1. IIS Manager > Server Certificates
2. Import o Complete Certificate Request
3. Seleccionar archivo .pfx
4. Ingresar contraseña

### 3. Agregar Binding HTTPS

1. IIS Manager > Sites > Ross Crafts
2. Bindings > Add
3. Configurar:
   - **Type:** https
   - **Port:** 443
   - **SSL certificate:** Seleccionar certificado
4. OK

### 4. Forzar HTTPS

Ya configurado en `settings/production.py`:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📊 Monitoreo y Mantenimiento

### 1. Logs de la Aplicación

Ubicación: `C:\inetpub\wwwroot\ross_crafts\logs\`

```bash
# Ver logs en tiempo real
Get-Content logs\activity.log -Wait -Tail 50
Get-Content logs\errors.log -Wait -Tail 50
```

### 2. Logs de IIS

Ubicación: `C:\inetpub\logs\LogFiles\`

### 3. Backup de Base de Datos

**Manual:**
```sql
BACKUP DATABASE ross_crafts_db 
TO DISK = 'C:\Backups\ross_crafts_db.bak' 
WITH INIT;
```

**Automático:**
Ver sección de backup en `scripts\setup_production_db.sql`

### 4. Actualizar Aplicación

```bash
cd C:\inetpub\wwwroot\ross_crafts
git pull origin main
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate --settings=settings.production
python manage.py collectstatic --noinput --settings=settings.production
iisreset
```

### 5. Monitoreo de Recursos

**Task Manager:**
- CPU, RAM, Disco
- Procesos de Python y SQL Server

**Performance Monitor:**
- Contadores de IIS
- Contadores de SQL Server

---

## 🐛 Solución de Problemas

### Error 500 - Internal Server Error

**Causa:** Error en la aplicación Django

**Solución:**
1. Revisar `logs\errors.log`
2. Verificar `DEBUG=False` en `.env`
3. Verificar `ALLOWED_HOSTS` incluye el dominio
4. Ejecutar: `python manage.py check --deploy --settings=settings.production`

### Error 503 - Service Unavailable

**Causa:** IIS no puede iniciar la aplicación

**Solución:**
1. Verificar que Python está instalado
2. Verificar ruta en `web.config`
3. Verificar permisos de IIS_IUSRS
4. Revisar Event Viewer de Windows

### No se puede conectar a SQL Server

**Solución:**
1. Verificar que SQL Server está ejecutándose
2. Verificar nombre del servidor en `.env`
3. Verificar permisos del usuario de IIS
4. Ejecutar: `python scripts\check_db.py`

### Archivos estáticos no se cargan

**Solución:**
1. Ejecutar: `python manage.py collectstatic --settings=settings.production`
2. Verificar permisos en carpeta `staticfiles`
3. Verificar configuración de MIME types en IIS

### Stripe webhook no funciona

**Solución:**
1. Verificar que la URL del webhook es accesible públicamente
2. Verificar `STRIPE_WEBHOOK_SECRET` en `.env`
3. Revisar logs de Stripe Dashboard
4. Verificar que el endpoint es HTTPS

### Emails no se envían

**Solución:**
1. Verificar credenciales de email en `.env`
2. Usar "App Password" de Gmail (no contraseña normal)
3. Habilitar "Acceso de apps menos seguras" si es necesario
4. Revisar `logs\errors.log`

---

## ✅ Checklist de Despliegue

### Pre-Despliegue
- [ ] Servidor Windows configurado
- [ ] SQL Server Express instalado
- [ ] ODBC Driver 17 instalado
- [ ] Python 3.12+ instalado
- [ ] IIS instalado y configurado
- [ ] Certificado SSL obtenido

### Configuración
- [ ] Base de datos creada
- [ ] Permisos de SQL Server configurados
- [ ] Variables de entorno configuradas (`.env`)
- [ ] `SECRET_KEY` generada
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Claves de Stripe LIVE configuradas

### Despliegue
- [ ] Código clonado en servidor
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] `deploy.bat` ejecutado exitosamente
- [ ] Superusuario creado
- [ ] Sitio web creado en IIS
- [ ] `web.config` configurado
- [ ] Permisos de archivos configurados

### Post-Despliegue
- [ ] Sitio accesible vía HTTP
- [ ] HTTPS configurado y funcionando
- [ ] Login de staff funciona
- [ ] Login de clientes funciona
- [ ] POS funciona correctamente
- [ ] Checkout y pagos funcionan
- [ ] Emails se envían correctamente
- [ ] Reportes se generan correctamente
- [ ] Backup automático configurado

### Monitoreo
- [ ] Logs configurados
- [ ] Monitoreo de recursos activo
- [ ] Plan de backup establecido
- [ ] Documentación actualizada

---

## 📞 Soporte

Para soporte técnico:
- **Email:** admin@rosscrafts.com
- **Documentación:** Ver archivos `GUIA_*.md`

---

**¡Despliegue completado! 🎉**
