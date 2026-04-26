# 🚀 Comandos Rápidos para Pruebas - Ross Crafts

## Ejecutar Pruebas

### Todas las pruebas
```bash
python manage.py test --settings=settings.test apps
```

### Por aplicación
```bash
python manage.py test --settings=settings.test apps.authentication
python manage.py test --settings=settings.test apps.stock
python manage.py test --settings=settings.test apps.sales
python manage.py test --settings=settings.test apps.ecommerce
python manage.py test --settings=settings.test apps.reports
python manage.py test --settings=settings.test apps.customers
python manage.py test --settings=settings.test apps.suppliers
python manage.py test --settings=settings.test apps.payments
python manage.py test --settings=settings.test apps.audit
```

### Prueba específica
```bash
python manage.py test --settings=settings.test apps.stock.tests.StockTests.test_producto_creado_correctamente
```

---

## Coverage

### Ejecutar con coverage
```bash
coverage run --source='apps' manage.py test --settings=settings.test apps
```

### Ver reporte
```bash
coverage report
```

### Generar HTML
```bash
coverage html
start htmlcov\index.html
```

### Limpiar archivos de coverage
```bash
del .coverage
rmdir /s /q htmlcov
```

---

## Scripts Automatizados

### Ejecutar todas las pruebas con coverage
```bash
run_tests.bat
```

### Ejecutar pruebas de una app específica
```bash
run_specific_test.bat authentication
run_specific_test.bat stock
run_specific_test.bat sales
```

---

## Configuración SQL Server

### Dar permisos para crear BD de pruebas
```sql
USE master;
GO

GRANT CREATE DATABASE TO [DOMINIO\Usuario];
GO
```

---

## GitHub Actions

### Ver estado de pruebas
1. Ir a la pestaña "Actions" en GitHub
2. Ver el último workflow ejecutado

### Descargar reporte de coverage
1. Ir a "Actions" > Workflow ejecutado
2. Descargar artefacto "coverage-report"

---

## Solución Rápida de Problemas

### Error: No se puede crear BD
```sql
GRANT CREATE DATABASE TO [DOMINIO\Usuario];
```

### Error: Module 'coverage' not found
```bash
pip install coverage
```

### Error: DATABASES not configured
```bash
# Asegúrate de usar --settings=settings.test
python manage.py test --settings=settings.test apps
```

---

## Verificar Configuración

### Verificar que settings/test.py existe
```bash
dir settings\test.py
```

### Verificar que .coveragerc existe
```bash
dir .coveragerc
```

### Verificar permisos SQL Server
```sql
SELECT HAS_PERMS_BY_NAME(NULL, NULL, 'CREATE DATABASE');
-- Debe retornar 1
```

---

## Comandos de Desarrollo

### Crear nueva prueba
1. Abrir `apps/[app_name]/tests.py`
2. Agregar nueva clase o método de prueba
3. Ejecutar: `python manage.py test --settings=settings.test apps.[app_name]`

### Ver pruebas disponibles
```bash
python manage.py test --settings=settings.test apps --verbosity=2
```

### Ejecutar con más detalle
```bash
python manage.py test --settings=settings.test apps --verbosity=3
```

---

**¡Comandos listos para usar! 🎯**
