@echo off
REM Script para verificar la configuración de tests

echo Verificando configuracion de pruebas...
echo.

REM Activar entorno virtual si existe
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

python check_test_setup.py

pause
