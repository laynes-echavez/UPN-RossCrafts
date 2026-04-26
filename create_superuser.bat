@echo off
echo ========================================
echo   Ross Crafts - Crear Superusuario
echo ========================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate

REM Crear superusuario
python manage.py createsuperuser

pause
