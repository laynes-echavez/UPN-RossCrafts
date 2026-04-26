@echo off
echo ========================================
echo   Ross Crafts - Iniciando Servidor
echo ========================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate

REM Verificar instalación
echo Verificando configuracion...
python manage.py check
echo.

REM Iniciar servidor
echo Iniciando servidor de desarrollo...
echo.
echo Accede a:
echo   - Aplicacion: http://localhost:8000/
echo   - Admin: http://localhost:8000/admin/
echo.
python manage.py runserver

pause
