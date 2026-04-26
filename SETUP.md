# Guía de Configuración - Ross Crafts

## Requisitos Previos

1. **Python 3.12+** instalado
2. **SQL Server Express** con instancia `ARJAY-LAYNES\SQLEXPRESS01`
3. **ODBC Driver 17 for SQL Server** instalado

## Pasos de Instalación

### 1. Crear Entorno Virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Crear Base de Datos

Ejecutar el script `create_database.sql` en SQL Server Management Studio o Azure Data Studio:

```sql
CREATE DATABASE ross_crafts_db COLLATE Modern_Spanish_CI_AS;
GO
USE ross_crafts_db;
GO
```

### 4. Verificar Conexión a SQL Server

```bash
python verify_connection.py
```

Si la conexión es exitosa, verás:
```
✓ Conexión exitosa a SQL Server
✓ Conexión: <pyodbc.Connection object>
✓ Versión de SQL Server: ...
✓ Conexión cerrada correctamente
```

### 5. Configurar Variables de Entorno

El archivo `.env` ya está creado. Actualiza los valores según sea necesario:

- `SECRET_KEY`: Genera una nueva clave secreta para producción
- `STRIPE_*`: Configura tus claves de Stripe
- `EMAIL_*`: Configura tu servidor SMTP

### 6. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 8. Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 9. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

Accede a:
- **Aplicación**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/

## Comandos Útiles

### Crear Migraciones
```bash
python manage.py makemigrations
```

### Aplicar Migraciones
```bash
python manage.py migrate
```

### Crear Superusuario
```bash
python manage.py createsuperuser
```

### Shell de Django
```bash
python manage.py shell
```

### Verificar Configuración
```bash
python manage.py check
```

## Estructura de Apps

- **authentication**: Gestión de usuarios y roles del sistema
- **stock**: Gestión de productos y control de stock
- **customers**: Gestión de clientes
- **suppliers**: Proveedores y órdenes de compra
- **sales**: Ventas presenciales / POS
- **reports**: Dashboard y reportes
- **ecommerce**: Tienda online pública
- **payments**: Pasarela de pagos Stripe
- **audit**: Registro de auditoría de acciones

## Configuración de Producción

Para producción, usa:

```bash
export DJANGO_SETTINGS_MODULE=settings.production
```

O en Windows:
```bash
set DJANGO_SETTINGS_MODULE=settings.production
```

## Solución de Problemas

### Error de Conexión a SQL Server

Si obtienes un error de conexión, verifica:

1. SQL Server está ejecutándose
2. La instancia `SQLEXPRESS01` existe
3. ODBC Driver 17 está instalado
4. Autenticación de Windows está habilitada

### Error de Importación de Módulos

Asegúrate de que el entorno virtual está activado:
```bash
venv\Scripts\activate
```

### Error de Migraciones

Si hay problemas con las migraciones, puedes resetear:
```bash
python manage.py migrate --fake-initial
```
