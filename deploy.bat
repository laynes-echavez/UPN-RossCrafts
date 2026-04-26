@echo off
REM Script de despliegue para Ross Crafts en Windows Server
REM Ejecutar como administrador o con permisos suficientes

echo ========================================
echo DESPLIEGUE ROSS CRAFTS - PRODUCCION
echo ========================================
echo.

REM Verificar que estamos en el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: No se encontro el entorno virtual
    echo Por favor ejecuta: python -m venv venv
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

echo [1/7] Verificando conexion a base de datos...
python scripts\check_db.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se puede conectar a SQL Server. Abortando despliegue.
    echo Por favor verifica la configuracion en .env
    pause
    exit /b 1
)

echo.
echo [2/7] Instalando/actualizando dependencias...
pip install -r requirements.txt --quiet

echo.
echo [3/7] Aplicando migraciones de base de datos...
python manage.py migrate --settings=settings.production
if %errorlevel% neq 0 (
    echo ERROR: Fallo al aplicar migraciones
    pause
    exit /b 1
)

echo.
echo [4/7] Recolectando archivos estaticos...
python manage.py collectstatic --noinput --settings=settings.production
if %errorlevel% neq 0 (
    echo ERROR: Fallo al recolectar archivos estaticos
    pause
    exit /b 1
)

echo.
echo [5/7] Cargando datos iniciales...
python manage.py loaddata apps\stock\fixtures\initial_categories.json --settings=settings.production
if %errorlevel% neq 0 (
    echo ADVERTENCIA: No se pudieron cargar las categorias iniciales
    echo Esto es normal si ya existen datos en la base de datos
)

echo.
echo [6/7] Verificando configuracion del sistema...
python manage.py check --settings=settings.production --deploy
if %errorlevel% neq 0 (
    echo ADVERTENCIA: Se encontraron problemas en la verificacion
    echo Revisa los mensajes anteriores
)

echo.
echo [7/7] Creando directorios necesarios...
if not exist "logs" mkdir logs
if not exist "media" mkdir media
if not exist "staticfiles" mkdir staticfiles

echo.
echo ========================================
echo DESPLIEGUE COMPLETADO EXITOSAMENTE
echo ========================================
echo.
echo Proximos pasos:
echo 1. Configurar IIS para servir la aplicacion
echo 2. Configurar certificado SSL
echo 3. Crear superusuario: python manage.py createsuperuser --settings=settings.production
echo 4. Verificar logs en: logs\
echo.

pause
