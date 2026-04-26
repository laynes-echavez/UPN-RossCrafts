@echo off
REM Script para ejecutar pruebas específicas

if "%1"=="" (
    echo Uso: run_specific_test.bat [app_name]
    echo.
    echo Ejemplos:
    echo   run_specific_test.bat authentication
    echo   run_specific_test.bat stock
    echo   run_specific_test.bat sales
    echo.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Ejecutando pruebas de apps.%1...
python manage.py test --settings=settings.test apps.%1.tests

pause
