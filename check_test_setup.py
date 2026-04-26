"""
Script para verificar que el entorno de pruebas está configurado correctamente
"""
import sys
import os

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("  ⚠ Se recomienda Python 3.10 o superior")
        return False
    return True

def check_django():
    """Verificar instalación de Django"""
    try:
        import django
        print(f"✓ Django {django.get_version()}")
        return True
    except ImportError:
        print("✗ Django no está instalado")
        print("  Ejecuta: pip install -r requirements.txt")
        return False

def check_coverage():
    """Verificar instalación de coverage"""
    try:
        import coverage
        print(f"✓ Coverage {coverage.__version__}")
        return True
    except ImportError:
        print("✗ Coverage no está instalado")
        print("  Ejecuta: pip install coverage")
        return False

def check_database_driver():
    """Verificar driver de SQL Server"""
    try:
        import pyodbc
        print(f"✓ pyodbc instalado")
        drivers = pyodbc.drivers()
        if 'ODBC Driver 17 for SQL Server' in drivers:
            print("✓ ODBC Driver 17 for SQL Server encontrado")
            return True
        else:
            print("⚠ ODBC Driver 17 for SQL Server no encontrado")
            print("  Drivers disponibles:", drivers)
            return False
    except ImportError:
        print("✗ pyodbc no está instalado")
        return False

def check_test_settings():
    """Verificar archivo de configuración de tests"""
    if os.path.exists('settings/test.py'):
        print("✓ settings/test.py existe")
        return True
    else:
        print("✗ settings/test.py no encontrado")
        return False

def check_test_files():
    """Verificar archivos de tests"""
    apps = ['authentication', 'stock', 'sales', 'ecommerce', 'reports', 
            'payments', 'audit', 'customers', 'suppliers']
    
    missing = []
    for app in apps:
        test_file = f'apps/{app}/tests.py'
        if os.path.exists(test_file):
            print(f"✓ {test_file}")
        else:
            print(f"✗ {test_file} no encontrado")
            missing.append(test_file)
    
    return len(missing) == 0

def check_coverage_config():
    """Verificar configuración de coverage"""
    if os.path.exists('.coveragerc'):
        print("✓ .coveragerc existe")
        return True
    else:
        print("✗ .coveragerc no encontrado")
        return False

def check_github_actions():
    """Verificar configuración de GitHub Actions"""
    if os.path.exists('.github/workflows/tests.yml'):
        print("✓ .github/workflows/tests.yml existe")
        return True
    else:
        print("✗ .github/workflows/tests.yml no encontrado")
        return False

def main():
    """Ejecutar todas las verificaciones"""
    print("=" * 60)
    print("Verificando configuración de pruebas - Ross Crafts")
    print("=" * 60)
    print()
    
    checks = [
        ("Versión de Python", check_python_version),
        ("Django", check_django),
        ("Coverage", check_coverage),
        ("Driver de Base de Datos", check_database_driver),
        ("Configuración de Tests", check_test_settings),
        ("Archivos de Tests", check_test_files),
        ("Configuración de Coverage", check_coverage_config),
        ("GitHub Actions", check_github_actions),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 60)
        results.append(check_func())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Resultado: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        print("✓ ¡Todo listo para ejecutar tests!")
        print("\nEjecuta: run_tests.bat")
    else:
        print("⚠ Hay problemas que resolver antes de ejecutar tests")
        print("\nRevisa los mensajes arriba para más detalles")
    
    print("=" * 60)
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
