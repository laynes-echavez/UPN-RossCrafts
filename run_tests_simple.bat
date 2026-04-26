@echo off
REM Script simple para ejecutar tests sin coverage

echo Ejecutando tests...

REM Activar entorno virtual si existe
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

python manage.py test --settings=settings.test apps

pause
