@echo off
REM Script para ejecutar pruebas automatizadas en Ross Crafts

echo ========================================
echo ROSS CRAFTS - PRUEBAS AUTOMATIZADAS
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

echo [1/4] Instalando dependencias de testing...
pip install coverage

echo.
echo [2/4] Ejecutando pruebas con coverage...
coverage run --source=apps manage.py test --settings=settings.test apps

echo.
echo [3/4] Generando reporte de cobertura...
coverage report

echo.
echo [4/4] Generando reporte HTML...
coverage html

echo.
echo ========================================
echo PRUEBAS COMPLETADAS
echo ========================================
echo.
echo Reporte HTML generado en: htmlcov\index.html
echo.
echo Para ver el reporte HTML, ejecuta:
echo start htmlcov\index.html
echo.

pause
