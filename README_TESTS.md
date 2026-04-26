# 🧪 Sistema de Pruebas Automatizadas - Ross Crafts

## 🎯 Resumen Ejecutivo

Este proyecto cuenta con un sistema completo de pruebas automatizadas que incluye:

- ✅ **200+ tests** cubriendo todos los módulos
- ✅ **Coverage objetivo: 70%+**
- ✅ **CI/CD** con GitHub Actions
- ✅ **Scripts de ejecución** para Windows
- ✅ **Documentación completa**

---

## 🚀 Inicio Rápido (3 pasos)

### 1. Verificar Configuración
```bash
check_setup.bat
```

### 2. Instalar Dependencias (si es necesario)
```bash
pip install -r requirements.txt
```

### 3. Ejecutar Tests
```bash
run_tests.bat
```

¡Listo! Los resultados aparecerán en consola y en `htmlcov/index.html`

---

## 📁 Estructura de Archivos

```
ross_crafts/
├── apps/
│   ├── authentication/tests.py    # Tests de autenticación
│   ├── stock/tests.py             # Tests de inventario
│   ├── sales/tests.py             # Tests de ventas
│   ├── ecommerce/tests.py         # Tests de tienda online
│   ├── payments/tests.py          # Tests de pagos
│   ├── reports/tests.py           # Tests de reportes
│   ├── audit/tests.py             # Tests de auditoría
│   ├── customers/tests.py         # Tests de clientes
│   └── suppliers/tests.py         # Tests de proveedores
├── settings/
│   └── test.py                    # Configuración para tests
├── .github/
│   └── workflows/
│       └── tests.yml              # CI/CD con GitHub Actions
├── .coveragerc                    # Configuración de coverage
├── run_tests.bat                  # Ejecutar todos los tests
├── run_tests_simple.bat           # Tests sin coverage
├── run_specific_test.bat          # Test específico
├── check_setup.bat                # Verificar configuración
├── TESTS_COMPLETADO.md            # Documentación técnica
└── GUIA_TESTS.md                  # Guía de usuario
```

---

## 🎮 Scripts Disponibles

### `run_tests.bat` (Recomendado)
Ejecuta todos los tests con coverage y genera reportes.
```bash
run_tests.bat
```

### `run_tests_simple.bat`
Ejecuta tests sin coverage (más rápido).
```bash
run_tests_simple.bat
```

### `run_specific_test.bat`
Ejecuta un test específico.
```bash
run_specific_test.bat apps.authentication.tests.AuthenticationTests
```

### `check_setup.bat`
Verifica que todo esté configurado correctamente.
```bash
check_setup.bat
```

---

## 📊 Cobertura de Tests

### Por Módulo

| Módulo | Tests | Descripción |
|--------|-------|-------------|
| **Authentication** | 10+ | Login, logout, roles, permisos |
| **Stock** | 15+ | Productos, categorías, movimientos |
| **Sales** | 12+ | Ventas, comprobantes, stock |
| **Ecommerce** | 15+ | Carrito, checkout, Stripe |
| **Reports** | 10+ | Reportes, exportación PDF/Excel |
| **Payments** | 5+ | Pagos, integración Stripe |
| **Audit** | 8+ | Logs, middleware, permisos |
| **Customers** | 8+ | Clientes, autenticación |
| **Suppliers** | 5+ | Proveedores, CRUD |

### Objetivo de Coverage
- **Mínimo**: 70%
- **Objetivo**: 80%+
- **Ideal**: 90%+

---

## 🔧 Configuración

### Base de Datos de Tests

Los tests usan una base de datos separada que se crea y destruye automáticamente:

```python
# settings/test.py
DATABASES['default']['TEST'] = {
    'NAME': 'ross_crafts_test_db',
}
```

**Requisitos:**
- Usuario de Windows con permisos `CREATE DATABASE`
- SQL Server Express instalado
- ODBC Driver 17 for SQL Server

### Solución de Problemas de Permisos

Si obtienes errores de permisos, ejecuta en SQL Server:

```sql
USE master;
GO
GRANT CREATE ANY DATABASE TO [TU_USUARIO_WINDOWS];
GO
```

---

## 🤖 CI/CD con GitHub Actions

### Configuración Automática

El archivo `.github/workflows/tests.yml` ejecuta automáticamente:

- ✅ Tests en cada push a `main` o `develop`
- ✅ Tests en cada pull request
- ✅ Generación de reporte de coverage
- ✅ Falla si coverage < 70%

### Ver Resultados

1. Ve a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Selecciona el workflow "Django Tests"
4. Descarga el artifact "coverage-report"

---

## 📖 Documentación

### Para Usuarios
- **GUIA_TESTS.md** - Guía completa de uso
- **README_TESTS.md** - Este archivo (resumen)

### Para Desarrolladores
- **TESTS_COMPLETADO.md** - Documentación técnica detallada
- Comentarios en código de tests

---

## 🎯 Casos de Uso Comunes

### Antes de Hacer Commit
```bash
run_tests.bat
# Verificar que todos pasen
git add .
git commit -m "Tu mensaje"
```

### Después de Agregar Funcionalidad
```bash
# 1. Escribir el test
# 2. Ejecutar solo ese test
run_specific_test.bat apps.stock.tests.StockTests.test_nueva_funcionalidad

# 3. Si pasa, ejecutar todos
run_tests.bat
```

### Verificar Coverage de un Módulo
```bash
coverage run --source=apps.stock manage.py test --settings=settings.test apps.stock
coverage report
```

### Debugging de Test que Falla
```bash
# 1. Ejecutar solo ese test con verbosidad
python manage.py test --settings=settings.test apps.stock.tests.StockTests.test_que_falla --verbosity=2

# 2. Mantener BD para inspección
python manage.py test --settings=settings.test apps.stock.tests.StockTests.test_que_falla --keepdb
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'coverage'"
```bash
pip install coverage
```

### Error: "Database creation failed"
Ver sección "Solución de Problemas de Permisos" arriba.

### Tests Muy Lentos
Ya está optimizado en `settings/test.py`:
```python
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
```

### Error: "ImportError: No module named 'apps'"
Asegúrate de estar en la raíz del proyecto:
```bash
cd C:\ruta\a\ross_crafts
run_tests.bat
```

---

## 📈 Mejores Prácticas

### 1. Ejecutar Tests Frecuentemente
- Antes de cada commit
- Después de cambios importantes
- Al menos una vez al día

### 2. Mantener Coverage Alto
- Objetivo: 70%+
- Agregar tests para código nuevo
- Revisar reporte HTML regularmente

### 3. Tests Independientes
- Cada test debe funcionar solo
- No depender del orden de ejecución
- Usar `setUp()` para datos frescos

### 4. Nombres Descriptivos
```python
# ✓ Bueno
def test_empleado_no_puede_acceder_a_reportes(self):

# ✗ Malo
def test_1(self):
```

### 5. Un Test, Una Cosa
```python
# ✓ Bueno
def test_login_exitoso(self):
    # Solo prueba login exitoso

def test_login_credenciales_incorrectas(self):
    # Solo prueba credenciales incorrectas

# ✗ Malo
def test_login(self):
    # Prueba muchas cosas a la vez
```

---

## 🎓 Aprender Más

### Documentación
- [GUIA_TESTS.md](GUIA_TESTS.md) - Guía completa con ejemplos
- [TESTS_COMPLETADO.md](TESTS_COMPLETADO.md) - Documentación técnica

### Recursos Externos
- [Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Python unittest](https://docs.python.org/3/library/unittest.html)

---

## ✅ Checklist de Verificación

Antes de considerar que los tests están completos:

- [ ] Todos los tests pasan
- [ ] Coverage > 70%
- [ ] Documentación actualizada
- [ ] Scripts funcionan correctamente
- [ ] GitHub Actions configurado
- [ ] Sin warnings importantes

---

## 🎉 ¡Listo para Usar!

El sistema de pruebas está completamente configurado y listo para usar.

**Comando principal:**
```bash
run_tests.bat
```

**Verificar configuración:**
```bash
check_setup.bat
```

**Ver guía completa:**
```bash
# Abrir GUIA_TESTS.md
```

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa [GUIA_TESTS.md](GUIA_TESTS.md) - Sección "Solución de Problemas"
2. Ejecuta `check_setup.bat` para diagnóstico
3. Revisa los logs de error detalladamente
4. Consulta la documentación de Django Testing

---

## 📝 Notas Finales

- Los tests usan una BD separada que se crea/destruye automáticamente
- Stripe está mockeado (no se hacen llamadas reales)
- Los emails usan backend en memoria (no se envían realmente)
- El coverage excluye migrations, admin.py, __init__.py, etc.

**¡Happy Testing!** 🚀
