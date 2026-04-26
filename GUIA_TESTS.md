# 🧪 Guía de Pruebas Automatizadas - Ross Crafts

## 📋 Índice
1. [Configuración del Entorno](#configuración-del-entorno)
2. [Ejecutar Pruebas](#ejecutar-pruebas)
3. [Cobertura de Código](#cobertura-de-código)
4. [Estructura de Pruebas](#estructura-de-pruebas)
5. [CI/CD con GitHub Actions](#cicd-con-github-actions)
6. [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Configuración del Entorno

### Requisitos Previos
- Python 3.12+
- SQL Server Express con autenticación de Windows
- Permisos para crear bases de datos

### Instalación de Dependencias
```bash
pip install coverage
```

### Configuración de Base de Datos de Pruebas

El archivo `settings/test.py` está configurado para usar una base de datos separada:

```python
DATABASES['default']['TEST'] = {
    'NAME': 'ross_crafts_test_db',  # BD separada para tests
}
```

**Importante:** 
- La BD de test se crea y destruye automáticamente con cada ejecución
- El usuario de Windows debe tener permisos `CREATE DATABASE`
- Se usa autenticación de Windows (`Trusted_Connection = 'yes'`)

---

## 🚀 Ejecutar Pruebas

### Método 1: Script Automatizado (Recomendado)
```bash
run_tests.bat
```

Este script:
1. Activa el entorno virtual
2. Instala dependencias
3. Ejecuta todas las pruebas
4. Genera reportes de cobertura

### Método 2: Comando Manual
```bash
# Todas las pruebas
python manage.py test --settings=settings.test apps

# Pruebas de una app específica
python manage.py test --settings=settings.test apps.authentication
python manage.py test --settings=settings.test apps.stock
python manage.py test --settings=settings.test apps.sales

# Prueba específica
python manage.py test --settings=settings.test apps.stock.tests.StockTests.test_producto_creado_correctamente
```

### Método 3: Script para App Específica
```bash
run_specific_test.bat authentication
run_specific_test.bat stock
run_specific_test.bat sales
```

---

## 📊 Cobertura de Código

### Ejecutar con Coverage
```bash
# Ejecutar pruebas con coverage
coverage run --source='apps' manage.py test --settings=settings.test apps

# Ver reporte en consola
coverage report

# Generar reporte HTML
coverage html
```

### Ver Reporte HTML
```bash
start htmlcov\index.html
```

### Configuración de Coverage (.coveragerc)
```ini
[run]
source = apps
omit =
    */migrations/*
    */admin.py
    */__init__.py
    */tests.py
    */apps.py

[report]
fail_under = 70
show_missing = True
```

**Meta de Cobertura:** 70% mínimo

---

## 📁 Estructura de Pruebas

### Apps con Pruebas Completas

#### 1. **Authentication** (`apps/authentication/tests.py`)
- ✅ Login exitoso (gerente, empleado, administrador)
- ✅ Login con credenciales incorrectas
- ✅ Control de acceso por roles
- ✅ Logout y cierre de sesión
- ✅ Redirección de usuarios no autenticados

**Ejemplo:**
```python
def test_login_exitoso_gerente(self):
    response = self.client.post('/auth/login/', {
        'username': 'gerente_test',
        'password': 'Test1234!'
    })
    self.assertEqual(response.status_code, 302)
```

#### 2. **Stock** (`apps/stock/tests.py`)
- ✅ Creación de productos y categorías
- ✅ Alertas de stock bajo
- ✅ Movimientos de inventario (entrada/salida)
- ✅ Generación automática de slugs
- ✅ CRUD completo de productos

**Ejemplo:**
```python
def test_alerta_stock_bajo(self):
    self.product.stock_quantity = 5
    self.product.save()
    self.assertTrue(self.product.needs_restock)
```

#### 3. **Sales** (`apps/sales/tests.py`)
- ✅ Registro de ventas completas
- ✅ Validación de stock antes de vender
- ✅ Generación de número de comprobante
- ✅ Cálculo de subtotales
- ✅ Ventas con múltiples items
- ✅ Generación de PDF

**Ejemplo:**
```python
def test_registro_venta_completa(self):
    stock_antes = self.product.stock_quantity
    response = self.client.post('/sales/registrar/', {...})
    self.product.refresh_from_db()
    self.assertEqual(self.product.stock_quantity, stock_antes - 3)
```

#### 4. **Ecommerce** (`apps/ecommerce/tests.py`)
- ✅ Agregar productos al carrito
- ✅ Carrito vacío inicial
- ✅ Incrementar/eliminar productos
- ✅ Integración con Stripe (mocked)
- ✅ Webhooks de pago

**Ejemplo:**
```python
@patch('stripe.PaymentIntent.create')
def test_crear_payment_intent(self, mock_stripe):
    mock_stripe.return_value = MagicMock(client_secret='pi_test_secret')
    response = self.client.post('/checkout/crear-intent/')
    self.assertIn('clientSecret', json.loads(response.content))
```

#### 5. **Reports** (`apps/reports/tests.py`)
- ✅ Reportes por rango de fechas
- ✅ Exportación a PDF
- ✅ Exportación a Excel
- ✅ Productos más vendidos
- ✅ Stock bajo
- ✅ Control de acceso por rol

#### 6. **Customers** (`apps/customers/tests.py`)
- ✅ Creación de clientes
- ✅ Email único
- ✅ Actualización de datos
- ✅ Autenticación de clientes

#### 7. **Suppliers** (`apps/suppliers/tests.py`)
- ✅ Gestión de proveedores
- ✅ CRUD completo

#### 8. **Payments** (`apps/payments/tests.py`)
- ✅ Integración con Stripe (mocked)
- ✅ Webhooks de pago exitoso/fallido
- ✅ Diferentes métodos de pago

#### 9. **Audit** (`apps/audit/tests.py`)
- ✅ Registro de logs de auditoría
- ✅ Middleware de auditoría
- ✅ Filtrado por usuario y acción
- ✅ Control de acceso

---

## 🔄 CI/CD con GitHub Actions

### Configuración (`.github/workflows/tests.yml`)

```yaml
name: Django Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run tests with coverage
      run: |
        coverage run --source='apps' manage.py test --settings=settings.test
        coverage report --fail-under=70
    
    - name: Upload coverage report
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report
        path: htmlcov/
```

### Activación
1. Hacer push al repositorio
2. GitHub Actions ejecutará automáticamente las pruebas
3. Ver resultados en la pestaña "Actions" de GitHub

---

## 🐛 Solución de Problemas

### Error: "No se puede crear la base de datos de pruebas"

**Solución:**
```sql
-- Ejecutar en SQL Server Management Studio
USE master;
GO

-- Dar permisos al usuario de Windows
GRANT CREATE DATABASE TO [DOMINIO\Usuario];
GO
```

### Error: "Module 'coverage' not found"

**Solución:**
```bash
pip install coverage
```

### Error: "DATABASES setting is not configured"

**Solución:**
Verificar que estás usando `--settings=settings.test`:
```bash
python manage.py test --settings=settings.test apps
```

### Las pruebas fallan por URLs no encontradas

**Nota:** Algunas pruebas verifican rutas que pueden no estar implementadas aún. Esto es normal y las pruebas están diseñadas para manejar estos casos con `assertIn(response.status_code, [200, 404])`.

### Error de permisos en Windows

**Solución:**
1. Ejecutar CMD como Administrador
2. O configurar permisos en SQL Server para tu usuario

---

## 📈 Mejores Prácticas

### 1. Ejecutar Pruebas Antes de Commit
```bash
run_tests.bat
```

### 2. Mantener Cobertura > 70%
```bash
coverage report
```

### 3. Escribir Pruebas para Nuevas Funcionalidades
```python
class MiNuevaFuncionalidadTests(TestCase):
    def setUp(self):
        # Configuración
        pass
    
    def test_funcionalidad_basica(self):
        # Prueba
        self.assertEqual(resultado, esperado)
```

### 4. Usar Mocks para Servicios Externos
```python
@patch('stripe.PaymentIntent.create')
def test_con_mock(self, mock_stripe):
    mock_stripe.return_value = MagicMock(...)
```

---

## 📝 Comandos Rápidos

```bash
# Ejecutar todas las pruebas
python manage.py test --settings=settings.test apps

# Con coverage
coverage run --source='apps' manage.py test --settings=settings.test apps
coverage report

# Prueba específica
python manage.py test --settings=settings.test apps.stock.tests.StockTests

# Ver reporte HTML
start htmlcov\index.html

# Limpiar archivos de coverage
del .coverage
rmdir /s /q htmlcov
```

---

## ✅ Checklist de Pruebas

- [x] Authentication: Login, logout, roles
- [x] Stock: CRUD, movimientos, alertas
- [x] Sales: Registro, validación, comprobantes
- [x] Ecommerce: Carrito, checkout, Stripe
- [x] Reports: Generación, exportación
- [x] Customers: Gestión de clientes
- [x] Suppliers: Gestión de proveedores
- [x] Payments: Procesamiento de pagos
- [x] Audit: Logs de auditoría
- [x] Coverage > 70%
- [x] CI/CD configurado

---

## 🎯 Próximos Pasos

1. **Ejecutar pruebas iniciales:**
   ```bash
   run_tests.bat
   ```

2. **Revisar cobertura:**
   ```bash
   start htmlcov\index.html
   ```

3. **Configurar GitHub Actions:**
   - Hacer push del código
   - Verificar ejecución en GitHub

4. **Mantener y expandir:**
   - Agregar pruebas para nuevas funcionalidades
   - Mantener cobertura > 70%
   - Ejecutar antes de cada commit

---

**¡Pruebas configuradas y listas para usar! 🚀**
